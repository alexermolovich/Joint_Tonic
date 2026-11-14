"""Bound the untrusted trajectory crossing from the evaluator to visualization."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('worker_preview_checks', ROOT/'apps/worker/server.py')
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
HOME = [0, 0, 0, -1.57079, 0, 1.57079, -.7853]


class PreviewChecks(unittest.TestCase):
    def payload(self, rows=None):
        return {'kind': 'fr3-joint-trajectory-v1', 'q': rows if rows is not None else [HOME.copy(), HOME.copy()]}

    def test_limits_and_filtered_payload(self):
        rows = [[limits[side] for limits in worker.FR3_LIMITS] for side in (0, 1)]
        payload = self.payload(rows)
        payload['untrusted_extra'] = {'path': '/etc/passwd'}
        result = worker.validated_preview(payload)
        self.assertEqual(result, self.payload(rows))
        self.assertEqual(len(worker.validated_preview(self.payload([HOME.copy() for _ in range(101)]))['q']), 101)

    def test_invalid_dimensions_and_envelope(self):
        for payload in [None, [], {}, {'kind': 'other', 'q': [HOME, HOME]}, self.payload([]), self.payload([HOME]),
                        self.payload([HOME]*102), self.payload([HOME, [0]*6]), self.payload([HOME, None])]:
            with self.subTest(payload=repr(payload)[:80]):
                self.assertIsNone(worker.validated_preview(payload))

    def test_values_are_finite_numbers_in_model_limits(self):
        for index in range(7):
            lo, hi = worker.FR3_LIMITS[index]
            for invalid in [True, False, None, '0', float('nan'), float('inf'), -float('inf'), lo-.001, hi+.001, 10**1000]:
                row = HOME.copy(); row[index] = invalid
                with self.subTest(joint=index, value=repr(invalid)[:30]):
                    self.assertIsNone(worker.validated_preview(self.payload([HOME, row])))


if __name__ == '__main__':
    unittest.main()
