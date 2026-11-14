---
{
  "schema_version": 1,
  "problem_id": "detect-dropped-duplicated-sensor-frames",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Detect Dropped and Duplicated Sensor Frames",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.audit_frame_ids",
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "physical_contract": {
    "frames": [
      "not-spatial"
    ],
    "units": {
      "frame_ids": "integer sequence counter"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "Log order is capture order; counters do not wrap or reset within one call.",
    "batching": "Nondecreasing integer-valued (N,) -> dict with int64 missing(K,) and duplicates(J,)."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-input",
      "independent-oracle",
      "immutability"
    ],
    "performance_class": "cpu",
    "evaluator_sha256": "a3515b95c216eb7e6652c0c4b160740899b4176d28c5c57d709a96b7392805d0"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original robotics-foundation exercise; no paper headline result or external dataset.",
    "primary_urls": [],
    "implementation_urls": []
  },
  "summary": "Report missing frame identifiers and repeated identifiers in an ordered sensor log.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "sensor-time"
  ],
  "paper_sections": [],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Detect Dropped and Duplicated Sensor Frames

Report missing frame identifiers and repeated identifiers in an ordered sensor log.

```python
def audit_frame_ids(frame_ids):
```

## Contract

Frame IDs must be a nondecreasing vector of integers in [0,100000]. Integer-valued floating inputs are accepted. Return a dict with `missing`: every absent ID between the first and last observed IDs, ascending; and `duplicates`: each ID occurring more than once, once, ascending. Empty input returns two empty int64 arrays. No losses before/after the observed range are inferred.

**Shapes and outputs:** Nondecreasing integer-valued (N,) -> dict with int64 missing(K,) and duplicates(J,).

**Units:** frame_ids: integer sequence counter. **Time:** Log order is capture order; counters do not wrap or reset within one call.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `[3,4,4,6]` â†’ `{"missing": [5], "duplicates": [4]}`.
2. `[7,7,7]` â†’ `{"missing": [], "duplicates": [7]}`; the repeated ID is listed once.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
