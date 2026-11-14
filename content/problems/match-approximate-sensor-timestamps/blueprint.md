---
{
  "schema_version": 1,
  "problem_id": "match-approximate-sensor-timestamps",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Match Approximate Sensor Timestamps",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.match_timestamps",
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
      "times": "seconds",
      "tolerance": "seconds"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "One common monotonic clock in seconds.",
    "batching": "reference (N,), queries (M,); output int64 (M,)."
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
    "evaluator_sha256": "94941104cdf8126e74844adaf32af3727e827c246621fa682b25efd1cd3bb6a4"
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
  "summary": "Associate each query with its nearest reference timestamp within a fixed tolerance.",
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

# Match Approximate Sensor Timestamps

Associate each query with its nearest reference timestamp within a fixed tolerance.

```python
def match_timestamps(reference, queries, tolerance):
```

## Contract

Reference times are strictly increasing; either vector may be empty. Tolerance is a nonnegative scalar. Match each query independently; reference reuse is allowed. Nearest-time ties choose the lower index. Return -1 if the absolute offset exceeds tolerance. Queries need not be sorted.

**Shapes and outputs:** reference (N,), queries (M,); output int64 (M,).

**Units:** times: seconds, tolerance: seconds. **Time:** One common monotonic clock in seconds.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `reference=[0,1,2], queries=[0.1,0.5,1.9], tolerance=0.2` â†’ `[0,-1,2]`. The middle sample is too far from both neighbors.
2. `reference=[0,2], queries=[1,0,2], tolerance=1` â†’ `[0,0,1]`. The exact midpoint uses the earlier reference.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
