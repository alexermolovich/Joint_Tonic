---
{
  "schema_version": 1,
  "problem_id": "planar-ik-jacobian-pseudoinverse",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Solve IK with a Jacobian Pseudoinverse",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.solve_planar_ik",
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
      "fixed right-handed base xy plane"
    ],
    "units": {
      "lengths,target": "metres",
      "angles,max_step": "radians",
      "tolerance": "metres"
    },
    "axes": "Both revolute joints rotate around +z; second angle is relative to first.",
    "timestamp_assumptions": "Static target; iterations are numerical steps, not physical timesteps.",
    "batching": "lengths(2,), initial_q(2,), target(2,), scalar controls -> (float64 q(2,), bool converged, float64 errors(K,))."
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
    "evaluator_sha256": "3be9e938a724e588b48a35ce857e593d0629442e8686bb170d6d1c055f759bc6"
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
  "summary": "Iteratively solve planar two-link position IK using a bounded pseudoinverse update.",
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
    "serial-chain-forward-kinematics",
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

# Solve IK with a Jacobian Pseudoinverse

Iteratively solve planar two-link position IK using a bounded pseudoinverse update.

```python
def solve_planar_ik(lengths, initial_q, target, max_iterations, tolerance, max_step):
```

## Contract

Lengths positive. max_iterations is integer 0..200, not bool. tolerance and max_step are positive scalar values. At each state, record Euclidean endpoint error. Stop if error<=tolerance or all updates are used. Otherwise compute dq=pinv(J,rcond=1e-12)@(target-endpoint), scale dq only if its norm exceeds max_step, and add it to q. Return final q without wrapping, convergence bool, and error history containing initial plus every updated state (length 1..max_iterations+1). No joint limits, collision tests, damping, line search, or restarts.

**Shapes and outputs:** lengths(2,), initial_q(2,), target(2,), scalar controls -> (float64 q(2,), bool converged, float64 errors(K,)).

**Units:** lengths,target: metres, angles,max_step: radians, tolerance: metres. **Time:** Static target; iterations are numerical steps, not physical timesteps.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `lengths=[1,1], initial_q=[0,pi/2], target=[1,1], max_iterations=20, tolerance=1e-6, max_step=0.5` returns the initial q, True, and a one-element near-zero error history.
2. `lengths=[1,1], initial_q=[0,0], target=[3,0], max_iterations=2, tolerance=1e-6, max_step=0.5` returns `[0,0]`, False, errors `[1,1,1]`; the straight arm cannot move outward.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Each link length must be at least 1e-9 metres; smaller values raise ValueError.
