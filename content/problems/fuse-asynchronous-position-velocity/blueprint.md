---
{
  "schema_version": 1,
  "problem_id": "fuse-asynchronous-position-velocity",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Fuse Asynchronous Position and Velocity Sensors",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.fuse_async_sensors",
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
      "one fixed world axis"
    ],
    "units": {
      "state": "position metres, velocity metres/second",
      "time": "seconds",
      "variances": "m\u00b2 for position, m\u00b2/s\u00b2 for velocity",
      "spectral_density": "m\u00b2/s\u00b3"
    },
    "axes": "Positive position and velocity share the same axis.",
    "timestamp_assumptions": "Nondecreasing event timestamps >=start_time. Simultaneous events are processed in supplied row order.",
    "batching": "x(2,), P(2,2), events(N,3), variances(N,) -> means float64(N,2), covariances float64(N,2,2)."
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
    "evaluator_sha256": "18d6b418342b5495a226198e57376094862b30daab23bd8ce5bf17fab5931642"
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
  "summary": "Predict to each sensor timestamp and fuse scalar position or velocity observations in arrival order.",
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
    "kalman-filter-predict-step",
    "kalman-filter-measurement-update"
  ],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Fuse Asynchronous Position and Velocity Sensors

Predict to each sensor timestamp and fuse scalar position or velocity observations in arrival order.

```python
def fuse_async_sensors(x, P, start_time, events, variances, spectral_density):
```

## Contract

Each event is [timestamp,kind,value], kind=0 position or 1 velocity. Measurement variances must be >1e-10. spectral_density q is a nonnegative scalar. Covariances must be symmetric within absolute tolerance 1e-10 and positive semidefinite (eigenvalues >=-1e-10); use their symmetrized values. Use constant velocity with continuous white acceleration: F=[[1,dt],[0,1]], Q=q*[[dtÂ³/3,dtÂ²/2],[dtÂ²/2,dt]]. Fuse each scalar observation with the corresponding row of identity and Joseph covariance. Return posterior states after every event. Empty event arrays (0,3) return correctly shaped empty outputs.

**Shapes and outputs:** x(2,), P(2,2), events(N,3), variances(N,) -> means float64(N,2), covariances float64(N,2,2).

**Units:** state: position metres, velocity metres/second, time: seconds, variances: mÂ² for position, mÂ²/sÂ² for velocity, spectral_density: mÂ²/sÂ³. **Time:** Nondecreasing event timestamps >=start_time. Simultaneous events are processed in supplied row order.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `x=[0,0], P=eye(2), start_time=0, events=[[0,0,2],[0,1,4]], variances=[1,1], spectral_density=0` â†’ means `[[1,0],[1,2]]`, covariances `[diag([0.5,1]),diag([0.5,0.5])]`.
2. `x=[0,1], P=zeros((2,2)), start_time=0, events=[[2,0,2]], variances=[1], spectral_density=0` â†’ means `[[2,1]]`, covariance all zeros.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
