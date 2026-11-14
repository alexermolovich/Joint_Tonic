"""Exercise the actual Linux bubblewrap runner with trusted adversarial fixtures.

Run in WSL with the project's Python 3.12 environment:
    /home/alex/.venvs/joint-tonic/bin/python tests/worker_checks.py

This checks OS containment and evaluator transport. It does not establish a
hostile-code anti-cheating boundary for tests sharing one Python interpreter.
"""
import importlib.util
import json
from pathlib import Path
import runpy
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('joint_tonic_worker_checks', ROOT/'apps/worker/server.py')
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
SLUG = 'se3-transform-points'
REFERENCE = (ROOT/'content/problems'/SLUG/'reference.py').read_text()
checks = []


def record(name, passed, **details):
    checks.append({'name': name, 'passed': bool(passed), **details})
    print(json.dumps(checks[-1]), flush=True)
    if not passed:
        raise AssertionError(name)


def run_reference_checks():
    totals = {'problems': 0, 'public': 0, 'hidden': 0}
    for folder in sorted((ROOT/'content/problems').iterdir()):
        if not (folder/'meta.json').exists():
            continue
        expected = runpy.run_path(str(folder/'cases.py'))['TESTS']
        result = worker.sandbox((folder/'reference.py').read_text(), folder.name, 'submit')
        failed = [t for t in result.get('tests', []) if not t['passed']]
        record('reference/'+folder.name, result.get('passed') and len(result['tests']) == len(expected),
               tests=len(result.get('tests', [])), failed=failed, error=result.get('error'))
        totals['problems'] += 1
        totals['public'] += sum(visibility == 'public' for _, visibility, _ in expected)
        totals['hidden'] += sum(visibility == 'hidden' for _, visibility, _ in expected)
    published = sum((folder/'meta.json').exists() for folder in (ROOT/'content/problems').iterdir() if folder.is_dir())
    record('reference/problem-count', totals['problems'] == published and published > 0, expected=published, **totals)
    result = worker.sandbox(REFERENCE, SLUG, 'run')
    record('public-only run', result.get('passed') and result['tests'] and all(t['visibility'] == 'public' for t in result['tests']),
           tests=len(result.get('tests', [])))
    return totals


def run_containment_checks():
    # Each assertion executes inside the real isolated learner process.
    probes = '''
import errno, os, resource, socket
assert not os.path.exists('/home/alex'), 'host home must not be mounted'
assert not os.path.exists('/mnt/c'), 'Windows filesystem must not be mounted'
assert os.environ.get('HOME') == '/tmp'
assert not any(k.startswith(('AWS_', 'SUPABASE_', 'VERCEL_')) for k in os.environ)
for address in [('1.1.1.1', 53), ('127.0.0.1', 8765)]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect(address)
    except OSError:
        pass
    else:
        raise AssertionError('network access unexpectedly succeeded')
    finally:
        sock.close()
try:
    with open('/work/should-not-exist.txt', 'w') as handle:
        handle.write('no')
except OSError as exc:
    assert exc.errno in (errno.EROFS, errno.EACCES, errno.EPERM)
else:
    raise AssertionError('/work must be read-only')
assert resource.getrlimit(resource.RLIMIT_CPU) == (10, 10)
assert resource.getrlimit(resource.RLIMIT_AS) == (4 * 1024**3, 4 * 1024**3)
assert resource.getrlimit(resource.RLIMIT_FSIZE) == (1024**2, 1024**2)
assert resource.getrlimit(resource.RLIMIT_NOFILE) == (64, 64)
assert resource.getrlimit(resource.RLIMIT_CORE) == (0, 0)
'''
    result = worker.sandbox(REFERENCE + probes, SLUG, 'submit')
    record('network/home/readonly/environment/resource containment', result.get('passed'), error=result.get('error'))

    result = worker.sandbox('def transform_points(T, points):\n    return None\n', SLUG, 'submit')
    record('wrong solution fails tests', not result.get('passed') and bool(result.get('tests')) and any(not t['passed'] for t in result['tests']),
           category=result.get('failure_category'))
    result = worker.sandbox('def broken(:\n', SLUG, 'submit')
    record('syntax errors reported', not result.get('passed') and 'SyntaxError' in result.get('error', ''), category=result.get('failure_category'))

    result = worker.sandbox("import sys, os\nsys.__stdout__.write('{\"passed\":true,\"tests\":[]}\\n')\nsys.__stdout__.flush()\nos._exit(0)\n", SLUG, 'submit')
    record('incomplete forged stdout report rejected', not result.get('passed') and result.get('failure_category') == 'learner-execution')

    result = worker.sandbox(REFERENCE + "\nprint('x' * 70000)\n", SLUG, 'submit')
    record('Python print output limit', not result.get('passed') and result.get('failure_category') == 'learner-output-limit')
    result = worker.sandbox("import os\nos.write(1, b'x' * 70000)\n", SLUG, 'submit')
    record('raw descriptor output limit', not result.get('passed') and result.get('failure_category') == 'learner-output-limit')

    result = worker.sandbox('while True:\n    pass\n', SLUG, 'submit')
    record('CPU limit terminates busy loop', not result.get('passed') and result.get('failure_category') == 'learner-resource-limit', category=result.get('failure_category'), exit_code=result.get('exit_code'))
    begin = time.monotonic()
    result = worker.sandbox('import time\ntime.sleep(40)\n', SLUG, 'submit')
    elapsed = time.monotonic() - begin
    record('wall timeout terminates sleeping code', not result.get('passed') and result.get('failure_category') == 'learner-timeout' and elapsed < 25,
           elapsed_seconds=round(elapsed, 2))


def run_http_checks():
    # A separate ephemeral port leaves the developer's existing worker alone.
    server = ThreadingHTTPServer(('127.0.0.1', 0), worker.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    owner = 'worker-check-owner-20261113'

    def request(path, body=None, identity=owner):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(base+path, data=data, headers={'Content-Type': 'application/json', 'X-Workspace-Id': identity})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as exc:
            return exc.code, json.load(exc)

    try:
        status, health = request('/health')
        record('HTTP health reports isolation', status == 200 and health.get('isolated') and health.get('sandbox') == 'bubblewrap')
        status, _ = request('/jobs', {'slug': '../outside', 'code': REFERENCE, 'mode': 'run'})
        record('HTTP rejects path traversal', status == 400)
        status, _ = request('/jobs', [])
        record('HTTP rejects non-object JSON', status == 400)
        status, accepted = request('/jobs', {'slug': SLUG, 'code': REFERENCE, 'mode': 'run'})
        record('HTTP queues job', status == 202 and accepted.get('status') == 'queued')
        job_id = accepted['id']
        status, _ = request('/jobs/'+job_id, identity='different-owner-20261113')
        record('HTTP enforces workspace ownership', status == 404)
        deadline = time.monotonic()+25
        while time.monotonic() < deadline:
            status, result = request('/jobs/'+job_id)
            if result.get('status') in ('completed', 'failed'):
                break
            time.sleep(.1)
        record('HTTP persists completed result and lineage', status == 200 and result.get('status') == 'completed' and result.get('passed') and result.get('lineage', {}).get('runtime') == worker.RUNTIME,
               status=result.get('status'), tests=len(result.get('tests', [])))
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    if sys.platform != 'linux':
        raise SystemExit('Run these checks in WSL/Linux; host learner-code execution is disabled.')
    totals = run_reference_checks()
    run_containment_checks()
    run_http_checks()
    print(json.dumps({'summary': {'checks': len(checks), 'passed': sum(c['passed'] for c in checks), 'reference_totals': totals},
                      'remaining_boundary': 'A local shared-interpreter evaluator is not an anti-cheating boundary. Learner code can inspect its own process and mounted evaluator; use a separate trusted evaluator protocol before public hostile submissions.'}), flush=True)
