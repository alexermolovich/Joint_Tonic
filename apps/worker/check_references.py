"""Author-owned reference tests; never executes user-submitted code."""
import importlib.util
import json
from pathlib import Path
import runpy
import sys

root=Path(__file__).resolve().parents[2]
failures=[];count=0;problems=0
for folder in sorted((root/'content/problems').iterdir()):
    if not (folder/'reference.py').exists(): continue
    spec=importlib.util.spec_from_file_location('reference',folder/'reference.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    tests=runpy.run_path(str(folder/'cases.py'))['TESTS'];problems+=1
    for name,visibility,check in tests:
        count+=1
        try: check(module)
        except BaseException as exc: failures.append(f'{folder.name}/{name}: {type(exc).__name__}: {exc}')
    print(f'{folder.name}: {len(tests)} checks')
print(json.dumps({'problems':problems,'tests':count,'failures':failures},indent=2))
sys.exit(1 if failures or problems!=10 else 0)
