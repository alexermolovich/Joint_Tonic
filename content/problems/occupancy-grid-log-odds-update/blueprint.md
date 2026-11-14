---
{
  "schema_version": 1,
  "problem_id": "occupancy-grid-log-odds-update",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Update Occupancy Grid Log Odds",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.update_occupancy",
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
      "grid row-column index frame"
    ],
    "units": {
      "log_odds": "dimensionless",
      "observations": "row, column, occupied probability",
      "prior": "occupied probability",
      "limit": "absolute log odds"
    },
    "axes": "Rows increase down; columns increase right. Cell dimensions are outside this component.",
    "timestamp_assumptions": "Observation rows are processed in arrival order; repeated cells accumulate evidence sequentially.",
    "batching": "log_odds(H,W), observations(N,3) -> fresh float64(H,W), H,W>=1."
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
    "evaluator_sha256": "ef3ccf7817158f4f23a448bd71d767800f2121d90ff734e43bb9e027fd044266"
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
  "summary": "Accumulate repeated occupancy observations in log-odds space with explicit clipping.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "mapping"
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

# Update Occupancy Grid Log Odds

Accumulate repeated occupancy observations in log-odds space with explicit clipping.

```python
def update_occupancy(log_odds, observations, prior, limit):
```

## Contract

Each observation row is [row,column,p], with integer-valued in-bounds indices and probability p strictly between 0 and 1. Prior is a scalar probability strictly between 0 and 1. Limit is a positive scalar; all initial log odds must lie in [-limit,limit]. For every observation, add log(p/(1-p))-log(prior/(1-prior)) to its cell, then clip immediately to [-limit,limit]. Unobserved cells are unchanged. Empty observations must have shape (0,3).

**Shapes and outputs:** log_odds(H,W), observations(N,3) -> fresh float64(H,W), H,W>=1.

**Units:** log_odds: dimensionless, observations: row, column, occupied probability, prior: occupied probability, limit: absolute log odds. **Time:** Observation rows are processed in arrival order; repeated cells accumulate evidence sequentially.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `log_odds=[[0]], observations=[[0,0,0.8],[0,0,0.8]], prior=0.5, limit=2` â†’ `[[2.0]]`.
2. `log_odds=[[0.3,-0.2]], observations=[[0,1,0.7]], prior=0.7, limit=4` â†’ `[[0.3,-0.2]]`; evidence equal to the prior is neutral.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
