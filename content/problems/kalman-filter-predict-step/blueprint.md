---
{
  "schema_version": 1,
  "problem_id": "kalman-filter-predict-step",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "One Kalman Filter Predict Step",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.kalman_predict",
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
      "one fixed right-handed world frame"
    ],
    "units": {
      "x": "declared state units",
      "P,Q": "products of state units",
      "F": "output-state/input-state units"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "F and Q already encode one chosen time interval.",
    "batching": "x(n,), P/F/Q(n,n), 1<=n<=32 -> (float64(n,),float64(n,n))."
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
    "evaluator_sha256": "ee7ab43afb91c7e3df9a546853b2a9ed2a9b80d758599423968561f400376270"
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
  "summary": "Propagate a linear robot state estimate and its covariance through one prediction interval.",
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

# One Kalman Filter Predict Step

Propagate a linear robot state estimate and its covariance through one prediction interval.

```python
def kalman_predict(x, P, F, Q):
```

## Contract

No control input is applied. F is any finite square matrix. Return predicted mean F@x and covariance F@P@F.T+Q, symmetrized to remove roundoff. Covariances must be symmetric within absolute tolerance 1e-10 and positive semidefinite (eigenvalues >=-1e-10); use their symmetrized values. n must be between 1 and 32. State components may mix position and velocity when F includes the appropriate seconds factors.

**Shapes and outputs:** x(n,), P/F/Q(n,n), 1<=n<=32 -> (float64(n,),float64(n,n)).

**Units:** x: declared state units, P,Q: products of state units, F: output-state/input-state units. **Time:** F and Q already encode one chosen time interval.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `x=[0,2], P=eye(2), F=[[1,1],[0,1]], Q=diag([0.1,0.2])` â†’ `([2,2], [[2.1,1],[1,1.2]])`.
2. `x=[3], P=[[2]], F=[[1]], Q=[[0]]` â†’ `([3],[[2]])`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
