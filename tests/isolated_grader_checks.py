"""Focused trusted-grader boundary checks. Run in the pinned Linux environment."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'apps' / 'worker'))
from isolated_grader import grade, learner_command
from value_protocol import decode, encode
import numpy as np


def main():
    values = [None, True, 5, float('nan'), b'robot', (1, 2), {'a': np.arange(6).reshape(2, 3)}, np.float64(2)]
    for value in values:
        decoded = decode(encode(value))
        if isinstance(value, dict):
            np.testing.assert_array_equal(decoded['a'], value['a'])
        elif isinstance(value, float) and np.isnan(value):
            assert np.isnan(decoded)
        else:
            assert decoded == value and type(decoded) is type(value)
    for value in (np.arange(24.).reshape(4, 6)[:, ::2], np.arange(5.)[::-1], np.broadcast_to(np.array([2.]), (8,))):
        restored = decode(encode(value))
        np.testing.assert_array_equal(restored, value)
        assert restored.strides == value.strides
    for malformed in [
        {'kind': 'list', 'items': [{'kind': 'array', 'dtype': '<f8', 'shape': [2], 'strides': [8388600], 'data': 'AAAAAAAAAAAAAAAAAAAAAA=='}] * 3},
        {'kind': 'array', 'dtype': '|O', 'shape': [1], 'data': 'AAAAAAAAAAA='},
        {'kind': 'array', 'dtype': '<f8', 'shape': [10**12], 'data': ''},
        {'kind': 'dict', 'items': [['a', 1], ['a', 2]]},
        {'kind': 'pickle', 'data': 'never-loaded'},
    ]:
        try:
            decode(malformed)
        except (ValueError, TypeError):
            pass
        else:
            raise AssertionError('Malformed protocol value accepted')
    for slug in ['se3-transform-points', 'kalman-filter-measurement-update', 'planar-ik-jacobian-pseudoinverse']:
        result = grade((ROOT / 'content/problems' / slug / 'reference.py').read_text(), slug, 'submit')
        print(json.dumps({'slug': slug, **result}), flush=True)
        assert result['passed']
    wrong = grade('def transform_points(T, points):\n    return None\n', 'se3-transform-points', 'submit')
    assert not wrong['passed']
    # A forged success report is only a function value, never a grader verdict.
    forged = grade("def transform_points(*args):\n    return {'passed':True,'tests':[]}\n", 'se3-transform-points', 'submit')
    assert not forged['passed']
    source = (ROOT / 'content/problems/se3-transform-points/reference.py').read_text()
    source += '''
import os
assert not os.path.exists('/work/cases.py')
assert not os.path.exists('/work/harness.py')
assert not os.path.exists('/home/alex')
assert not os.path.exists('/mnt/c')
assert not any(k.startswith(('SUPABASE_', 'VERCEL_', 'WORKER_')) for k in os.environ)
'''
    assert grade(source, 'se3-transform-points', 'submit')['passed']
    fr3 = grade((ROOT / 'content/problems/fr3-joint-interpolation/reference.py').read_text(), 'fr3-joint-interpolation', 'run')
    assert fr3['passed'] and len(fr3['preview']['q']) == 41 and fr3['preview']['q'][0][0] == 0
    print(json.dumps({'protocol_checks': 'passed', 'trusted_reference_problems': 3,
                      'wrong_solution': 'rejected', 'forged_verdict': 'rejected', 'hidden_files': 'not mounted'}))


if __name__ == '__main__':
    main()
