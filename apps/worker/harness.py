"""Trusted test harness copied into each disposable sandbox."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import resource
import runpy
import sys
import time

# Linux limits are inherited by imports and learner code.
resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
resource.setrlimit(resource.RLIMIT_FSIZE, (1024**2, 1024**2))
resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

class OutputLimitExceeded(Exception):
    pass


class LimitedLog(io.StringIO):
    def __init__(self):
        super().__init__()
        self.total_bytes = 0
        self.exceeded = False

    def write(self, value):
        self.total_bytes += len(value.encode('utf-8', errors='replace'))
        if self.total_bytes > 65536:
            self.exceeded = True
            raise OutputLimitExceeded('Output exceeded 64 KB. Reduce print output.')
        remaining = max(0, 16384 - self.tell())
        super().write(value[:remaining])
        return len(value)

started = time.monotonic()
logs = LimitedLog()
tests = []
error = None
failure_category = None
preview = None
preview_error = None
try:
    with contextlib.redirect_stdout(logs), contextlib.redirect_stderr(logs):
        suite = runpy.run_path('/work/cases.py')['TESTS']
        spec = importlib.util.spec_from_file_location('solution', '/work/solution.py')
        solution = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution)
        for name, visibility, check in suite:
            if visibility == 'hidden' and sys.argv[1] != 'submit':
                continue
            begin = time.monotonic()
            result = {'name': name, 'visibility': visibility, 'passed': False}
            try:
                check(solution)
                result['passed'] = True
            except OutputLimitExceeded:
                raise
            except BaseException as exc:
                result['message'] = f'{type(exc).__name__}: {exc}'[:1600] if visibility == 'public' else f'{type(exc).__name__}: Hidden case did not satisfy the documented contract.'
            result['duration_ms'] = round((time.monotonic() - begin) * 1000, 2)
            tests.append(result)
        # This optional module is an authored PUBLIC fixture. Learner code still
        # runs in this disposable sandbox; it never receives a simulator handle.
        if Path('/work/preview.py').is_file():
            try:
                preview = runpy.run_path('/work/preview.py')['build_preview'](solution)
                if len(json.dumps(preview, allow_nan=False)) > 20000:
                    raise ValueError('Preview exceeds the bounded trajectory size')
            except OutputLimitExceeded:
                raise
            except BaseException:
                preview = None
                preview_error = 'The public demonstration did not return a valid bounded joint trajectory.'
except BaseException as exc:
    error = f'{type(exc).__name__}: {exc}'[:2000]
    failure_category = 'learner-output-limit' if logs.exceeded else 'learner-import'

if logs.exceeded:
    error = 'Output exceeded 64 KB. Reduce print output.'
    failure_category = 'learner-output-limit'
elif not error and any(not test['passed'] for test in tests):
    failure_category = 'learner-tests'

print(json.dumps({'tests': tests, 'passed': bool(tests) and all(t['passed'] for t in tests) and not error,
                 'error': error, 'failure_category': failure_category,
                 'preview': preview, 'preview_error': preview_error,
                 'logs': logs.getvalue(), 'duration_ms': round((time.monotonic()-started)*1000, 2)}))
