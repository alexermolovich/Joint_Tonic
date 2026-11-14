"""Loopback-only job service. Learner Python runs exclusively inside bubblewrap."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / '.local' / 'jobs'
STORE.mkdir(parents=True, exist_ok=True)
VENV = os.environ.get('JOINT_TONIC_VENV', '/home/alex/.venvs/joint-tonic')
EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=2)
LOCK = threading.Lock()
ACTIVE = set()
RUNTIME = 'python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2'

def validate_report(report, expected_tests):
    """Validate transport structure; this is not a Python anti-cheating boundary."""
    if not isinstance(report, dict) or type(report.get('passed')) is not bool:
        raise ValueError('Invalid evaluator report')
    tests = report.get('tests')
    if not isinstance(tests, list) or len(tests) > len(expected_tests):
        raise ValueError('Invalid evaluator test count')
    if not isinstance(report.get('logs', ''), str) or report.get('error') is not None and not isinstance(report.get('error'), str):
        raise ValueError('Invalid evaluator diagnostics')
    actual = []
    for test in tests:
        if not isinstance(test, dict) or type(test.get('passed')) is not bool:
            raise ValueError('Invalid evaluator case')
        actual.append((test.get('name'), test.get('visibility')))
    if actual != expected_tests[:len(actual)]:
        raise ValueError('Evaluator case order did not match the published evaluator')
    if report['passed'] and (actual != expected_tests or not tests or report.get('error') or not all(t['passed'] for t in tests)):
        raise ValueError('Incomplete or inconsistent evaluator success report')
    return report

def save(job):
    target = STORE / (job['id'] + '.json')
    temp = target.with_suffix('.tmp')
    temp.write_text(json.dumps(job), encoding='utf-8')
    temp.replace(target)

def sandbox(code, slug, mode):
    if os.name != 'posix' or not shutil.which('bwrap'):
        raise RuntimeError('The isolated Linux runner is unavailable. Start the WSL worker; host execution is disabled.')
    problem = ROOT / 'content' / 'problems' / slug
    if mode not in ('run', 'submit'):
        raise ValueError('Invalid evaluation mode')
    expected_tests = [(name, visibility) for name, visibility, _ in runpy.run_path(str(problem/'cases.py'))['TESTS']
                      if visibility == 'public' or mode == 'submit']
    with tempfile.TemporaryDirectory(prefix='joint-tonic-') as temp:
        work = Path(temp)
        work.chmod(0o755)
        (work/'solution.py').write_text(code, encoding='utf-8')
        shutil.copyfile(problem/'cases.py', work/'cases.py')
        shutil.copyfile(ROOT/'apps/worker/harness.py', work/'harness.py')
        for file in work.iterdir(): file.chmod(0o444)
        command = ['bwrap','--unshare-all','--new-session','--die-with-parent','--cap-drop','ALL',
                   '--ro-bind','/usr','/usr','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64',
                   '--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin','--proc','/proc','--dev','/dev',
                   '--tmpfs','/tmp','--dir','/etc','--ro-bind','/etc/ld.so.cache','/etc/ld.so.cache',
                   '--ro-bind',VENV,'/opt/venv','--ro-bind',str(work),'/work','--chdir','/work',
                   '--clearenv','--setenv','PATH','/opt/venv/bin:/usr/bin','--setenv','HOME','/tmp',
                   '--setenv','OPENBLAS_NUM_THREADS','1','--setenv','OMP_NUM_THREADS','1',
                   '--setenv','MKL_NUM_THREADS','1','--setenv','PYTHONDONTWRITEBYTECODE','1',
                   '/opt/venv/bin/python','-I','/work/harness.py',mode]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
        chunks = bytearray()
        exceeded = threading.Event()
        def consume():
            while True:
                chunk = process.stdout.read(4096)
                if not chunk: break
                if len(chunks)+len(chunk)>65536:
                    exceeded.set()
                    try: os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError: pass
                    break
                chunks.extend(chunk)
        reader = threading.Thread(target=consume,daemon=True); reader.start()
        try: process.wait(timeout=18)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL); process.wait(); reader.join(2)
            return {'tests':[], 'passed':False, 'error':'Execution exceeded the 18-second wall-clock limit.', 'failure_category':'learner-timeout'}
        reader.join(2)
        if exceeded.is_set():
            return {'tests':[], 'passed':False,'error':'Output exceeded 64 KB. Reduce print output.','failure_category':'learner-output-limit'}
        raw=chunks.decode('utf-8',errors='replace')
        if process.returncode:
            # bubblewrap may forward a child's fatal signal as 128+signal.
            resource_exits = {-signal.SIGKILL, -signal.SIGXCPU, 128+signal.SIGKILL, 128+signal.SIGXCPU}
            category = 'learner-resource-limit' if process.returncode in resource_exits else 'learner-execution'
            return {'tests': [], 'passed': False, 'error': raw[-2000:] or 'Process reached a CPU/memory limit or exited without a result.', 'failure_category': category, 'exit_code': process.returncode}
        try: return validate_report(json.loads(raw.strip().splitlines()[-1]), expected_tests)
        except (ValueError,IndexError,TypeError):
            return {'tests':[], 'passed':False, 'error':raw[-2000:] or 'Process reached a CPU/memory limit or exited without a result.', 'failure_category':'learner-execution'}

def evaluate(job):
    try:
        job['status']='running'; save(job)
        result=sandbox(job['code'],job['slug'],job['mode'])
        job.update(result); job['status']='completed'
    except Exception as exc:
        job.update(status='failed',error=str(exc)[:2000],failure_category='platform')
    finally:
        save(job)
        with LOCK: ACTIVE.discard(job['id'])
        print(json.dumps({'event':'evaluation.completed','correlation_id':job['id'],'slug':job['slug'],'passed':job.get('passed'),'status':job['status']}),flush=True)

class Handler(BaseHTTPRequestHandler):
    def send(self, status, body):
        data=json.dumps(body).encode()
        self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers();self.wfile.write(data)
    def do_GET(self):
        if self.path=='/health': return self.send(200,{'ok':True,'sandbox':'bubblewrap','runtime':RUNTIME,'isolated':bool(shutil.which('bwrap'))})
        job_id=self.path.removeprefix('/jobs/')
        if not re.fullmatch(r'[a-f0-9-]{36}',job_id): return self.send(404,{'error':'Job not found'})
        file=STORE/(job_id+'.json')
        if not file.exists(): return self.send(404,{'error':'Job not found'})
        job=json.loads(file.read_text()); owner=self.headers.get('X-Workspace-Id','')
        if owner!=job.get('owner'): return self.send(404,{'error':'Job not found'})
        return self.send(200,{k:v for k,v in job.items() if k!='owner'})
    def do_POST(self):
        if self.path!='/jobs': return self.send(404,{'error':'Unknown endpoint'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<100000: return self.send(413,{'error':'Source must be less than 64 KB'})
            body=json.loads(self.rfile.read(length))
            if not isinstance(body,dict): return self.send(400,{'error':'Malformed request'})
            slug=body.get('slug',''); code=body.get('code'); mode=body.get('mode')
            if not re.fullmatch(r'[a-z0-9-]+',slug) or not (ROOT/'content/problems'/slug/'meta.json').exists(): return self.send(400,{'error':'Unknown problem'})
            if not isinstance(code,str) or len(code.encode())>65536 or mode not in ('run','submit'): return self.send(400,{'error':'Invalid source or mode'})
            owner=self.headers.get('X-Workspace-Id','')
            if not re.fullmatch(r'[a-zA-Z0-9-]{16,80}',owner): return self.send(400,{'error':'Missing local workspace identifier'})
            with LOCK:
                if len(ACTIVE)>=8: return self.send(429,{'error':'Runner is busy. Try again shortly.'})
                job_id=str(uuid4());ACTIVE.add(job_id)
            meta=json.loads((ROOT/'content/problems'/slug/'meta.json').read_text())
            digest=hashlib.sha256((ROOT/'content/problems'/slug/'cases.py').read_bytes()).hexdigest()
            job={'id':job_id,'slug':slug,'mode':mode,'owner':owner,'code':code,'status':'queued','created_at':datetime.now(timezone.utc).isoformat(),
                 'lineage':{'problem_version':meta['version'],'evaluator_sha256':digest,'runtime':RUNTIME,'fixture_version':'synthetic-1','seed':20261113,'source_sha256':hashlib.sha256(code.encode()).hexdigest()}}
            save(job);EXECUTOR.submit(evaluate,job)
            self.send(202,{'id':job_id,'status':'queued'})
        except (ValueError,KeyError,TypeError): self.send(400,{'error':'Malformed request'})
    def log_message(self, fmt, *args): pass

if __name__=='__main__':
    print('Joint Tonic isolated worker http://127.0.0.1:8765',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
