---
{
  "schema_version": 1,
  "problem_id": "mahalanobis-measurement-gate",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Gate Measurements with Mahalanobis Distance",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.gate_measurements",
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
      "residuals": "sensor units",
      "covariance": "products of sensor units",
      "threshold": "dimensionless squared distance"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "All residuals use the same measurement model and covariance at a common evaluation interval.",
    "batching": "residuals(N,D), covariance(D,D), scalar threshold -> (float64 distances(N,), bool accepted(N,)); 1<=D<=32."
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
    "evaluator_sha256": "29c15083833e369db24fe3b9dbf29e9c9c6f0df4f4a56f3ae3c266a51528cbd7"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original robotics-foundation exercise; no paper headline result or external dataset.",
    "primary_urls": [
      "https://www.cs.cmu.edu/~motionplanning/papers/sbp_papers/kalman/welch_intro_kalman.pdf"
    ],
    "implementation_urls": []
  },
  "summary": "Accept sensor innovations using their squared covariance-normalized distance.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "state-estimation"
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

# Gate Measurements with Mahalanobis Distance

Accept sensor innovations using their squared covariance-normalized distance.

```python
def gate_measurements(residuals, covariance, threshold):
```

## Contract

Covariance is symmetric within atol=1e-10; symmetrize it and require all eigenvalues >1e-10. Threshold is a nonnegative scalar. Distances are squared Mahalanobis distances. Accept equality at the threshold. Empty batches (0,D) are valid; D must be 1..32. No chi-square threshold selection is performed.

**Shapes and outputs:** residuals(N,D), covariance(D,D), scalar threshold -> (float64 distances(N,), bool accepted(N,)); 1<=D<=32.

**Units:** residuals: sensor units, covariance: products of sensor units, threshold: dimensionless squared distance. **Time:** All residuals use the same measurement model and covariance at a common evaluation interval.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `residuals=[[2,0],[0,2]], covariance=diag([4,1]), threshold=1` â†’ distances `[1,4]`, accepted `[True,False]`.
2. `residuals=[[0]], covariance=[[2]], threshold=0` â†’ `([0],[True])`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
