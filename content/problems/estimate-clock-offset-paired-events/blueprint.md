---
{
  "schema_version": 1,
  "problem_id": "estimate-clock-offset-paired-events",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Estimate Clock Offset from Paired Events",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.estimate_clock_offset",
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
      "timestamps": "seconds",
      "offset": "seconds",
      "residuals": "seconds"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "Rows are paired events; clock_b approximately equals clock_a plus offset. No rate drift is fitted.",
    "batching": "Two same-length nonempty (N,) -> (float offset, float64 residuals(N,))."
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
    "evaluator_sha256": "2f5be3b9a41983244ea7adfc7e36b05b5607349f960836a310e92fb294ef8457"
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
  "summary": "Estimate a constant clock offset from corresponding event timestamps using a robust median.",
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

# Estimate Clock Offset from Paired Events

Estimate a constant clock offset from corresponding event timestamps using a robust median.

```python
def estimate_clock_offset(clock_a, clock_b):
```

## Contract

Accept paired timestamps in any row order; length must agree and be positive. Offset is median(clock_b-clock_a), averaging the middle two differences for even N. Return residuals clock_b-clock_a-offset in original row order. Do not sort residuals. Timestamps need not be increasing because pairing is already supplied.

**Shapes and outputs:** Two same-length nonempty (N,) -> (float offset, float64 residuals(N,)).

**Units:** timestamps: seconds, offset: seconds, residuals: seconds. **Time:** Rows are paired events; clock_b approximately equals clock_a plus offset. No rate drift is fitted.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `clock_a=[0,1,2], clock_b=[2,3,11]` â†’ `(2.0,[0,0,7])`. One delayed event does not move the median.
2. `clock_a=[1,2], clock_b=[0,3]` â†’ `(0.0,[-1,1])`. The two middle differences average to zero.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
