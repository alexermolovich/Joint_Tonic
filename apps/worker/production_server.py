"""Authenticated loopback service for a separately hosted Linux/gVisor worker.

Only explicitly qualified data-protocol problem revisions may be submitted.
The development shared-interpreter runner is never a fallback.
"""
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

import server
from isolated_grader import grade


def configuration():
    token = os.environ.get('WORKER_SERVICE_TOKEN', '')
    image = os.environ.get('JOINT_TONIC_RUNTIME_IMAGE', '')
    if len(token) < 32:
        raise RuntimeError('WORKER_SERVICE_TOKEN must contain at least 32 characters')
    control = urlsplit(os.environ.get('CONTROL_PLANE_URL', ''))
    if control.scheme != 'https' or not control.hostname or control.username or control.query or control.fragment or control.path not in ('', '/'):
        raise RuntimeError('CONTROL_PLANE_URL must be an HTTPS web origin')
    if not re.fullmatch(r'[^\s]+@sha256:[a-f0-9]{64}', image):
        raise RuntimeError('A digest-pinned runtime image is required')
    manifest_path = Path(os.environ.get('JOINT_TONIC_QUALIFICATION', ''))
    if not manifest_path.is_file():
        raise RuntimeError('Run the gVisor qualification suite and provide its manifest')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('backend') != 'gvisor' or manifest.get('runtime_image') != image or not manifest.get('problems'):
        raise RuntimeError('Qualification manifest does not match this runtime')
    for filename, expected in manifest.get('grader_files', {}).items():
        if filename not in ('isolated_grader.py', 'value_protocol.py', 'learner_rpc.py'):
            raise RuntimeError('Unknown grader artifact')
        actual = hashlib.sha256((Path(__file__).parent / filename).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError('Grader changed after qualification')
    if len(manifest.get('grader_files', {})) != 3:
        raise RuntimeError('Incomplete grader artifact manifest')
    info = subprocess.run(['docker', 'info', '--format', '{{json .Runtimes}}'], capture_output=True, timeout=10, check=True)
    if 'runsc' not in json.loads(info.stdout):
        raise RuntimeError('Docker must have the runsc runtime configured')
    return token, image, manifest


def revision_matches(slug, qualified):
    if not re.fullmatch(r'[a-z0-9-]+', slug) or type(qualified) is not dict:
        return False
    folder = server.ROOT / 'content' / 'problems' / slug
    files = qualified.get('files')
    expected = {'meta.json', 'cases.py', 'reference.py', 'starter.py'}
    if (folder/'preview.py').exists():
        expected.add('preview.py')
    if type(files) is not dict or set(files) != expected:
        return False
    try:
        meta = json.loads((folder/'meta.json').read_text())
        contract = meta.get('execution_contract', {})
        if meta.get('version') != qualified.get('version') or contract.get('protocol') != 'data-only-functions-v1' or contract.get('semantics') != 'value-only' or not contract.get('reviewed_by'):
            return False
        return all(type(digest) is str and re.fullmatch(r'[a-f0-9]{64}', digest)
            and hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest for name, digest in files.items())
    except (ValueError, OSError):
        return False


def persist(job):
    """Only a trusted completed evaluation can reach the service-role RPC."""
    if job.get('grading_protocol') != 'data-only-functions-v1':
        return
    result_keys = ('passed', 'tests', 'logs', 'duration_ms', 'error', 'failure_category', 'lineage', 'preview', 'preview_error')
    payload = {'id': job['id'], 'user_id': job['owner'], 'slug': job['slug'],
        'version': job['lineage']['problem_version'], 'mode': job['mode'], 'status': job['status'],
        'code': job['code'], 'created_at': job['created_at'], 'started_at': job['started_at'],
        'finished_at': job['finished_at'], 'result': {k: job[k] for k in result_keys if k in job},
        'lineage': job['lineage']}
    key = os.environ['WORKER_SERVICE_TOKEN']
    request = Request(os.environ['CONTROL_PLANE_URL'].rstrip('/') + '/api/evaluations',
        data=json.dumps({'p_job': payload}).encode(), method='POST',
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    with urlopen(request, timeout=10) as response:
        if response.status not in (200, 201, 204):
            raise RuntimeError('Account history write failed')
    job['cloud_saved'] = True
    server.save(job)


def main():
    token, image, manifest = configuration()
    if not all(revision_matches(slug, item) for slug, item in manifest['problems'].items()):
        raise RuntimeError('Qualification has an incomplete, changed or incompatible content revision')
    scratch = os.environ.get('JOINT_TONIC_JOB_TMP')
    if not scratch or not Path(scratch).is_absolute():
        raise RuntimeError('Set an absolute shared host scratch directory for Docker bind mounts')
    Path(scratch).mkdir(parents=True, exist_ok=True, mode=0o700)
    server.RUNTIME = 'data-only-functions-v1:' + image.rsplit('@', 1)[1]

    def isolated(code, slug, mode):
        qualified = manifest['problems'].get(slug)
        if not qualified or not revision_matches(slug, qualified):
            raise RuntimeError('This content revision has not passed production qualification')
        result = grade(code, slug, mode, backend='gvisor')
        result['runtime_image_digest'] = image.rsplit('@', 1)[1]
        return result

    server.sandbox = isolated

    def evaluate(job):
        job['started_at'] = datetime.now(timezone.utc).isoformat()
        job['status'] = 'running'
        job['grading_protocol'] = 'data-only-functions-v1'
        job['lineage'].update(runtime_image_digest=image.rsplit('@', 1)[1],
            grading_protocol='data-only-functions-v1', fixture_sha256=job['lineage']['evaluator_sha256'])
        metadata = json.loads((server.ROOT/'content/problems'/job['slug']/'meta.json').read_text())
        job['lineage']['seed'] = metadata.get('grading', {}).get('seed', 20261113)
        job['lineage'].pop('harness_sha256', None)
        for name, digest in manifest['grader_files'].items():
            job['lineage'][name.removesuffix('.py') + '_sha256'] = digest
        server.save(job)
        try:
            job.update(isolated(job['code'], job['slug'], job['mode']))
            job['status'] = 'completed'
        except Exception:
            job.update(status='failed', passed=False, error='The qualified evaluator could not complete this revision.', failure_category='platform')
        finally:
            job['finished_at'] = datetime.now(timezone.utc).isoformat()
            job.setdefault('duration_ms', max(0, (datetime.fromisoformat(job['finished_at']) - datetime.fromisoformat(job['started_at'])).total_seconds() * 1000))
            server.save(job)
            with server.LOCK:
                server.ACTIVE.discard(job['id'])
        try:
            persist(job)
        except Exception:
            print(json.dumps({'event': 'account.history_pending', 'correlation_id': job['id']}), flush=True)
        print(json.dumps({'event': 'evaluation.completed', 'correlation_id': job['id'],
                          'status': job['status'], 'passed': job.get('passed')}), flush=True)

    server.evaluate = evaluate

    # A restarted host must not leave jobs permanently queued or rerun submissions
    # implicitly. Retained failures remain visible and can be retried by the user.
    for file in server.STORE.glob('*.json'):
        try:
            pending = json.loads(file.read_text())
            if pending.get('status') in ('queued', 'running') and pending.get('lineage', {}).get('runtime', '').startswith('data-only-functions-v1:'):
                pending.update(status='failed', passed=False, failure_category='platform',
                    error='The evaluator restarted before this job completed. Submit again.',
                    finished_at=datetime.now(timezone.utc).isoformat())
                server.save(pending)
        except (ValueError, OSError):
            pass

    def reconcile():
        while True:
            for file in server.STORE.glob('*.json'):
                try:
                    job = json.loads(file.read_text())
                    if job.get('grading_protocol') == 'data-only-functions-v1' and not job.get('cloud_saved') and job.get('finished_at'):
                        persist(job)
                except Exception:
                    pass  # Retry retained records; never log source, credentials or private errors.
            time.sleep(30)

    threading.Thread(target=reconcile, daemon=True).start()

    admission = threading.Lock()

    class Handler(server.Handler):
        def authorized(self):
            owner = self.headers.get('X-Account-Id', '')
            return (hmac.compare_digest(self.headers.get('Authorization', ''), 'Bearer ' + token)
                and re.fullmatch(r'[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}', owner)
                and self.headers.get('X-Workspace-Id') == owner)

        def do_GET(self):
            if not self.authorized():
                return self.send(401, {'error': 'Authenticated web proxy required'})
            return super().do_GET()

        def do_POST(self):
            if not self.authorized():
                return self.send(401, {'error': 'Authenticated web proxy required'})
            with admission:
                return self.admit()

        def admit(self):
            # Bound outstanding jobs per authenticated account as well as the
            # existing eight-job global queue; never trust a browser workspace ID.
            owner = self.headers.get('X-Account-Id')
            pending = 0
            for file in server.STORE.glob('*.json'):
                try:
                    job = json.loads(file.read_text())
                    pending += job.get('owner') == owner and job.get('status') in ('queued', 'running')
                except (ValueError, OSError):
                    continue
            if pending >= 2:
                return self.send(429, {'error': 'Two evaluations are already in progress for this account'})
            return super().do_POST()

    # Only a TLS reverse proxy may reach this loopback service. The Docker socket
    # belongs to the trusted host service and is never mounted into learner jobs.
    print(json.dumps({'event': 'production_worker.listening', 'runtime': server.RUNTIME,
                      'qualified_problems': len(manifest['problems'])}), flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8765), Handler).serve_forever()


if __name__ == '__main__':
    main()
