"""Trusted grading with a data-only learner boundary.

NumPy/Python function contracts only in v1. Autograd/object APIs are deliberately
unsupported until they have a reviewed transport; never fall back to shared tests.
"""
import json
import os
from pathlib import Path
import queue
import re
import runpy
import signal
import subprocess
import tempfile
import threading
import time
from uuid import uuid4

from value_protocol import MAX_BYTES, decode, encode

ROOT = Path(__file__).resolve().parents[2]
WORKER = Path(__file__).resolve().parent
EXCEPTIONS = {t.__name__: t for t in (ValueError, TypeError, IndexError, KeyError,
    RuntimeError, AssertionError, AttributeError, ZeroDivisionError, OverflowError)}


def learner_command(work, backend, container_name):
    if backend == 'gvisor':
        image = os.environ.get('JOINT_TONIC_RUNTIME_IMAGE', '')
        if not re.fullmatch(r'[^\s]+@sha256:[a-f0-9]{64}', image):
            raise RuntimeError('Set a digest-pinned JOINT_TONIC_RUNTIME_IMAGE')
        return ['docker', 'run', '--rm', '-i', '--name', container_name,
            '--runtime=runsc', '--network=none', '--read-only', '--user=65532:65532',
            '--cap-drop=ALL', '--security-opt=no-new-privileges', '--pids-limit=64',
            '--memory=4g', '--memory-swap=4g', '--cpus=1', '--ulimit=core=0',
            '--ulimit=nofile=64:64', '--ulimit=fsize=1048576:1048576',
            '--tmpfs=/tmp:rw,noexec,nosuid,size=64m', '--ipc=none',
            '--mount', f'type=bind,src={work},dst=/work,readonly',
            '--workdir=/work', '--env=HOME=/tmp', '--env=OPENBLAS_NUM_THREADS=1',
            '--env=OMP_NUM_THREADS=1', '--env=MKL_NUM_THREADS=1',
            '--env=PYTHONDONTWRITEBYTECODE=1', image, 'python', '-I', '/work/learner_rpc.py']
    if backend != 'bubblewrap' or os.name != 'posix':
        raise RuntimeError('Unsupported isolated transport backend')
    venv = os.environ.get('JOINT_TONIC_VENV', '/home/alex/.venvs/joint-tonic')
    return ['bwrap', '--unshare-all', '--new-session', '--die-with-parent', '--cap-drop', 'ALL',
        '--ro-bind', '/usr', '/usr', '--symlink', 'usr/lib', '/lib', '--symlink', 'usr/lib64', '/lib64',
        '--symlink', 'usr/bin', '/bin', '--symlink', 'usr/sbin', '/sbin', '--proc', '/proc', '--dev', '/dev',
        '--tmpfs', '/tmp', '--dir', '/etc', '--ro-bind', '/etc/ld.so.cache', '/etc/ld.so.cache',
        '--ro-bind', venv, '/opt/venv', '--ro-bind', str(work), '/work', '--chdir', '/work',
        '--clearenv', '--setenv', 'PATH', '/opt/venv/bin:/usr/bin', '--setenv', 'HOME', '/tmp',
        '--setenv', 'OPENBLAS_NUM_THREADS', '1', '--setenv', 'OMP_NUM_THREADS', '1',
        '--setenv', 'MKL_NUM_THREADS', '1', '--setenv', 'PYTHONDONTWRITEBYTECODE', '1',
        '/opt/venv/bin/python', '-I', '/work/learner_rpc.py']


class Learner:
    def __init__(self, code, backend='bubblewrap'):
        self.backend = backend
        self.container = 'jt-' + uuid4().hex
        self.directory = tempfile.TemporaryDirectory(prefix='joint-tonic-rpc-', dir=os.environ.get('JOINT_TONIC_JOB_TMP'))
        work = Path(self.directory.name)
        work.chmod(0o755)
        for name in ('learner_rpc.py', 'value_protocol.py'):
            (work / name).write_bytes((WORKER / name).read_bytes())
        (work / 'solution.py').write_text(code, encoding='utf-8')
        for file in work.iterdir():
            file.chmod(0o444)
        self.logs = ''
        self.deadline = time.monotonic() + 18
        self.messages = queue.Queue(maxsize=1)
        self.closed = False
        try:
            self.process = subprocess.Popen(learner_command(work, backend, self.container),
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, start_new_session=True)
        except BaseException:
            self.directory.cleanup()
            raise
        self.timer = threading.Timer(18, self.close)
        self.timer.daemon = True
        self.timer.start()
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        try:
            while not self.closed:
                line = self.process.stdout.readline(2 * MAX_BYTES + 1)
                if not line or len(line) > 2 * MAX_BYTES or not line.endswith(b'\n'):
                    raise RuntimeError('Learner disconnected or exceeded protocol output budget')
                self.messages.put(line, timeout=max(.01, self.deadline - time.monotonic()))
        except BaseException:
            try:
                self.messages.put_nowait(None)
            except queue.Full:
                pass

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        def call(*args, **kwargs):
            request_id = uuid4().hex
            payload = json.dumps({'id': request_id, 'function': name, 'args': encode(args),
                'kwargs': encode(kwargs)}, allow_nan=False, separators=(',', ':')).encode() + b'\n'
            if len(payload) > 2 * MAX_BYTES:
                raise RuntimeError('Function arguments exceed protocol budget')
            if self.closed:
                raise RuntimeError('Learner execution exceeded its wall-clock budget')
            try:
                self.process.stdin.write(payload)
                self.process.stdin.flush()
                line = self.messages.get(timeout=max(.01, self.deadline - time.monotonic()))
                if line is None:
                    raise RuntimeError('Learner process exited without a value')
                response = json.loads(line)
                if type(response) is not dict or response.get('id') != request_id:
                    raise RuntimeError('Invalid learner response identity')
                logs = response.get('logs', '')
                if not isinstance(logs, str) or len(logs.encode()) > 65536:
                    raise RuntimeError('Invalid learner logs')
                self.logs = (self.logs + logs).encode()[:16384].decode(errors='ignore')
                if 'exception' in response:
                    error_type = EXCEPTIONS.get(response['exception'], RuntimeError)
                    raise error_type(str(response.get('message', 'Learner exception'))[:1000])
                return decode(response['value'])
            except (BrokenPipeError, queue.Empty):
                raise RuntimeError('Learner process stopped or reached the time limit') from None
        return call

    def close(self):
        if self.closed:
            return
        self.closed = True
        if hasattr(self, 'timer'):
            self.timer.cancel()
        if self.backend == 'gvisor':
            try:
                result = subprocess.run(['docker', 'rm', '-f', self.container], timeout=10,
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if result.returncode:
                    print(json.dumps({'event': 'sandbox.cleanup_failed', 'container': self.container}), flush=True)
            except (OSError, subprocess.TimeoutExpired):
                print(json.dumps({'event': 'sandbox.cleanup_failed', 'container': self.container}), flush=True)
        if self.process.poll() is None:
            try:
                os.killpg(self.process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass
        self.process.stdin.close()
        self.process.stdout.close()
        self.directory.cleanup()


def grade(code, slug, mode, backend='bubblewrap'):
    if mode not in ('run', 'submit') or not re.fullmatch(r'[a-z0-9-]+', slug):
        raise ValueError('Invalid evaluation request')
    problem = ROOT / 'content' / 'problems' / slug
    tests = runpy.run_path(str(problem / 'cases.py'))['TESTS']
    started = time.monotonic()
    learner = Learner(code, backend)
    results = []
    try:
        for name, visibility, check in tests:
            if visibility != 'public' and mode != 'submit':
                continue
            begin = time.monotonic()
            result = {'name': name, 'visibility': visibility, 'passed': False}
            try:
                check(learner)
                result['passed'] = True
            except BaseException as exc:
                result['message'] = (f'{type(exc).__name__}: {exc}'[:1600] if visibility == 'public'
                    else f'{type(exc).__name__}: Hidden case did not satisfy the documented contract.')
            result['duration_ms'] = round((time.monotonic() - begin) * 1000, 2)
            results.append(result)
        report = {'tests': results, 'passed': bool(results) and all(t['passed'] for t in results),
            'logs': learner.logs, 'duration_ms': round((time.monotonic() - started) * 1000, 2),
            'grading_protocol': 'data-only-functions-v1', 'backend': backend}
        if slug == 'fr3-joint-interpolation':
            try:
                # The fixture stays trusted; only its function inputs enter the learner.
                report['preview'] = runpy.run_path(str(problem / 'preview.py'))['build_preview'](learner)
            except Exception:
                report['preview_error'] = 'The public demonstration did not return a valid bounded joint trajectory.'
        return report
    finally:
        learner.close()
