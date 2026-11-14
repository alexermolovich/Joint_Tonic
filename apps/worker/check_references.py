"""Check author-owned reference solutions, optionally inside the Linux sandbox.

Usage: python apps/worker/check_references.py [--sandbox] [problem-slug ...]
Never pass learner submissions to this authoring tool.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import runpy
import sys

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', action='store_true', help='Verify both Run and Submit using the isolated worker.')
    parser.add_argument('slugs', nargs='*', help='Published problem slugs; defaults to the whole catalog.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    catalog = {folder.name: folder for folder in sorted((root/'content/problems').iterdir())
               if folder.is_dir() and (folder/'meta.json').exists()}
    unknown = sorted(set(args.slugs) - catalog.keys())
    if unknown:
        parser.error('Unknown published problem(s): ' + ', '.join(unknown))
    selected = list(dict.fromkeys(args.slugs)) if args.slugs else list(catalog)
    failures = []
    count = 0
    if not selected:
        failures.append('No published problems found.')
    if args.sandbox:
        from server import sandbox
    for slug in selected:
        folder = catalog[slug]
        try:
            tests = runpy.run_path(str(folder/'cases.py'))['TESTS']
            if not tests or not any(v == 'public' for _, v, _ in tests) or not any(v == 'hidden' for _, v, _ in tests):
                raise ValueError('A problem needs both public and hidden tests.')
            if args.sandbox:
                code = (folder/'reference.py').read_text(encoding='utf-8')
                for mode in ('run', 'submit'):
                    result = sandbox(code, slug, mode)
                    expected = sum(v == 'public' or mode == 'submit' for _, v, _ in tests)
                    if not result.get('passed') or len(result.get('tests', [])) != expected:
                        failed = [test for test in result.get('tests', []) if not test.get('passed')]
                        failures.append(f'{slug}/{mode}: {result.get("error") or failed or "Unexpected test count"}')
            else:
                spec = importlib.util.spec_from_file_location('reference', folder/'reference.py')
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, _, check in tests:
                    try:
                        check(module)
                    except BaseException as exc:
                        failures.append(f'{slug}/{name}: {type(exc).__name__}: {exc}')
            count += len(tests)
            print(f'{slug}: {len(tests)} checks' + (' (isolated Run + Submit)' if args.sandbox else ''), flush=True)
        except Exception as exc:
            failures.append(f'{slug}: {type(exc).__name__}: {exc}')
    print(json.dumps({'problems': len(selected), 'tests': count, 'failures': failures}, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
