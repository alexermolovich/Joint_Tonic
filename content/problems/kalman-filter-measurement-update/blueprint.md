---
{
  "schema_version": 1,
  "problem_id": "kalman-filter-measurement-update",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "One Kalman Filter Measurement Update",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.kalman_update",
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
      "one fixed world frame with H mapping into sensor coordinates"
    ],
    "units": {
      "x": "state units",
      "z": "sensor units",
      "P": "products of state units",
      "R": "products of sensor units"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "Prior and measurement represent the same timestamp.",
    "batching": "x(n,), P(n,n), z(m,), H(m,n), R(m,m), 1<=n,m<=32 -> (mean(n,), covariance(n,n))."
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
    "evaluator_sha256": "e7c554a3904532da33e9ba025155c45e43a3ee52602b8568536edeabba4eceae"
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
  "summary": "Fuse a linear sensor measurement using a stable Kalman gain and Joseph covariance update.",
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
  "prerequisite_problem_ids": [
    "kalman-filter-predict-step"
  ],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# One Kalman Filter Measurement Update

Fuse a linear sensor measurement using a stable Kalman gain and Joseph covariance update.

```python
def kalman_update(x, P, z, H, R):
```

## Contract

Covariances must be symmetric within absolute tolerance 1e-10 and positive semidefinite (eigenvalues >=-1e-10); use their symmetrized values. R must additionally be strictly positive definite with eigenvalues >1e-10. Return updated float64 state and Joseph-form covariance, symmetrized. H maps the state to expected sensor readings; no bias term. Both state and measurement dimensions are between 1 and 32. Solve linear systems; an explicit inverse is unnecessary.

**Shapes and outputs:** x(n,), P(n,n), z(m,), H(m,n), R(m,m), 1<=n,m<=32 -> (mean(n,), covariance(n,n)).

**Units:** x: state units, z: sensor units, P: products of state units, R: products of sensor units. **Time:** Prior and measurement represent the same timestamp.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `x=[0], P=[[1]], z=[2], H=[[1]], R=[[1]]` â†’ `([1],[[0.5]])`.
2. `x=[3], P=[[0]], z=[10], H=[[1]], R=[[2]]` â†’ `([3],[[0]])`; an exactly known prior receives zero gain.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
