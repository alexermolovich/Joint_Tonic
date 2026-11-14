---
{
  "schema_version": 1,
  "problem_id": "damped-least-squares-ik-step",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Stabilize Singular IK with Damped Least Squares",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.damped_ik_step",
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
      "one common normalized task frame"
    ],
    "units": {
      "jacobian": "normalized task coordinate per normalized joint coordinate",
      "error": "normalized task coordinates",
      "damping": "task/joint scale ratio"
    },
    "axes": "Rows share caller-supplied metric scaling; mixed raw metres/radians must be scaled before calling.",
    "timestamp_assumptions": "One static linearized IK iteration, not a physical motion command.",
    "batching": "J(M,N), error(M,), scalar damping -> float64 correction(N,), residual(M,); 1<=M,N<=32."
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
    "evaluator_sha256": "3d51970a884ea1f33ced085feb335d4b4c8ef5631e2ff026c4f668c75a8cc549"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original robotics-foundation exercise; no paper headline result or external dataset.",
    "primary_urls": [
      "https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/"
    ],
    "implementation_urls": []
  },
  "summary": "Compute a regularized joint-space correction that remains bounded near singular Jacobians.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "inverse-kinematics"
  ],
  "paper_sections": [],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "geometric-jacobian-joint-axes"
  ],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Stabilize Singular IK with Damped Least Squares

Compute a regularized joint-space correction that remains bounded near singular Jacobians.

```python
def damped_ik_step(jacobian, error, damping):
```

## Contract

Damping is strictly positive. Solve the unique minimizer of ||J*dq-error||Â²+dampingÂ²||dq||Â². Return dq and predicted residual J@dq-error. Use singular-value filtering or a stable equivalent; avoid forming an inverse. The inputs are normalized coordinates with units/scales already made comparable by the caller. Zero and rank-deficient J are supported.

**Shapes and outputs:** J(M,N), error(M,), scalar damping -> float64 correction(N,), residual(M,); 1<=M,N<=32.

**Units:** jacobian: normalized task coordinate per normalized joint coordinate, error: normalized task coordinates, damping: task/joint scale ratio. **Time:** One static linearized IK iteration, not a physical motion command.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `jacobian=[[1,0],[0,0]], error=[2,3], damping=1` â†’ correction `[1,0]`, residual `[-1,-3]`.
2. `jacobian=[[1,1]], error=[2], damping=1` â†’ correction `[2/3,2/3]`, residual `[-2/3]`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Damping must be at least 1e-9; smaller values raise ValueError. This lower bound avoids underflow in the squared damping term.
