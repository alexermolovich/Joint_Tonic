"""Untrusted-side function server. Contains no cases, expected outputs or verdicts."""
import contextlib
import importlib.util
import io
import json
import os
import resource
import sys

sys.path.insert(0, '/work')
from value_protocol import MAX_BYTES, decode, encode

resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


class Logs(io.TextIOBase):
    def __init__(self):
        self.total = 0
        self.parts = []
        self.retained = 0

    def write(self, text):
        data = text.encode('utf-8', errors='replace')
        self.total += len(data)
        if self.total > 65536:
            raise RuntimeError('Learner output exceeded 64 KiB')
        kept = data[:max(0, 16384 - self.retained)]
        self.parts.append(kept.decode('utf-8', errors='ignore'))
        self.retained += len(kept)
        return len(text)


wire = os.fdopen(os.dup(1), 'w', buffering=1)
logs = Logs()
sys.stdout = sys.stderr = logs
spec = importlib.util.spec_from_file_location('solution', '/work/solution.py')
solution = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(solution)
    import_error = None
except BaseException as exc:
    import_error = type(exc).__name__

for line in sys.stdin:
    try:
        if len(line.encode()) > 2 * MAX_BYTES:
            raise ValueError('Request exceeds protocol budget')
        request = json.loads(line)
        if import_error:
            raise RuntimeError('Learner import failed: ' + import_error)
        name = request['function']
        if not isinstance(name, str) or not name.isidentifier() or name.startswith('_'):
            raise ValueError('Invalid function name')
        args, kwargs = decode(request['args']), decode(request['kwargs'])
        result = getattr(solution, name)(*args, **kwargs)
        response = {'id': request['id'], 'value': encode(result), 'logs': ''.join(logs.parts)}
    except BaseException as exc:
        response = {'id': request.get('id') if isinstance(locals().get('request'), dict) else None,
                    'exception': type(exc).__name__, 'message': str(exc)[:1000], 'logs': ''.join(logs.parts)}
    logs.parts.clear()
    encoded = json.dumps(response, allow_nan=False, separators=(',', ':'))
    if len(encoded.encode()) > 2 * MAX_BYTES:
        encoded = json.dumps({'id': response['id'], 'exception': 'RuntimeError', 'message': 'Return value exceeds protocol budget'})
    wire.write(encoded + '\n')
