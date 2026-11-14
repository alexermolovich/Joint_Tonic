"""Qualify explicit content revisions on a built gVisor image; no guessed digest."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from isolated_grader import ROOT, WORKER, grade

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('slugs', nargs='+')
args = parser.parse_args()
image = os.environ.get('JOINT_TONIC_RUNTIME_IMAGE', '')
manifest = {'backend': 'gvisor', 'runtime_image': image, 'protocol': 'data-only-functions-v1',
            'grader_files': {name: hashlib.sha256((WORKER/name).read_bytes()).hexdigest()
                for name in ('isolated_grader.py', 'value_protocol.py', 'learner_rpc.py')}, 'problems': {}}
for slug in args.slugs:
    if not __import__('re').fullmatch(r'[a-z0-9-]+', slug):
        raise ValueError('Invalid problem slug')
    folder = ROOT / 'content/problems' / slug
    meta = json.loads((folder/'meta.json').read_text())
    contract = meta.get('execution_contract', {})
    if contract.get('protocol') != 'data-only-functions-v1' or contract.get('semantics') != 'value-only' or not contract.get('reviewed_by'):
        raise RuntimeError(f'{slug}: no reviewed value-only execution contract. Existing native identity, aliasing, input-mutation and autograd contracts cannot be qualified by this transport. Review a separate content version; do not weaken its tests.')
    reference, starter = (folder/'reference.py').read_text(), (folder/'starter.py').read_text()
    for mode in ('run', 'submit'):
        result = grade(reference, slug, mode, 'gvisor')
        if not result['passed']:
            raise RuntimeError(f'{slug}: reference failed {mode}; do not enable this revision')
    if grade(starter, slug, 'submit', 'gvisor')['passed']:
        raise RuntimeError(f'{slug}: incomplete starter was accepted')
    name = meta['entrypoint'].split('.')[-1]
    wrong = f'def {name}(*args, **kwargs):\n    return {{"passed": True, "tests": []}}\n'
    if grade(wrong, slug, 'submit', 'gvisor')['passed']:
        raise RuntimeError(f'{slug}: forged report accepted')
    manifest['problems'][slug] = {'version': meta['version'], 'files': {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ('meta.json', 'cases.py', 'reference.py', 'starter.py')}}
    if (folder/'preview.py').is_file():
        manifest['problems'][slug]['files']['preview.py'] = hashlib.sha256((folder/'preview.py').read_bytes()).hexdigest()
    print(json.dumps({'event': 'runtime.qualified', 'slug': slug}), flush=True)
Path(args.output).write_text(json.dumps(manifest, indent=2) + '\n')
