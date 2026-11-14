---
{
  "schema_version": 1,
  "problem_id": "differential-drive-rollout",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute a Differential-Drive Rollout",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.differential_drive_rollout",
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
      "fixed right-handed world xy plane",
      "robot body forward x, left y"
    ],
    "units": {
      "pose": "x,y metres; yaw radians",
      "wheel_rates": "left,right radians/second",
      "dt": "seconds",
      "radius,track": "metres"
    },
    "axes": "Positive yaw is counterclockwise; faster right wheel increases yaw.",
    "timestamp_assumptions": "One common monotonic clock in seconds.",
    "batching": "initial_pose(3,), wheel_rates(T,2), dt/radius/track scalar -> float64(T+1,3)."
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
    "evaluator_sha256": "c5e28b2854533ef50824a2df479237f5004f7bcfd474abd86931106a81a909ee"
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
  "summary": "Integrate piecewise-constant wheel rates into an exact planar differential-drive pose sequence.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "planning-control"
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

# Compute a Differential-Drive Rollout

Integrate piecewise-constant wheel rates into an exact planar differential-drive pose sequence.

```python
def differential_drive_rollout(initial_pose, wheel_rates, dt, radius, track):
```

## Contract

dt, wheel radius and wheel-center track width are positive scalars. First output is the initial pose with yaw wrapped into [-pi,pi). Each rate row is held constant for dt. Use exact circular-arc integration; zero angular velocity must reduce continuously to straight motion. Every returned yaw is wrapped into [-pi,pi). Empty rate arrays (0,2) return one initial pose.

**Shapes and outputs:** initial_pose(3,), wheel_rates(T,2), dt/radius/track scalar -> float64(T+1,3).

**Units:** pose: x,y metres; yaw radians, wheel_rates: left,right radians/second, dt: seconds, radius,track: metres. **Time:** One common monotonic clock in seconds.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `initial_pose=[0,0,0], wheel_rates=[[1,1],[1,1]], dt=1, radius=1, track=2` â†’ `[[0,0,0],[1,0,0],[2,0,0]]`.
2. Same parameters with one rate row `[[0,2]]` â†’ final `[sin(1),1-cos(1),1]`, approximately `[0.84147098,0.45969769,1]`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

dt, radius and track must each be at least 1e-9 in their declared units; smaller values raise ValueError.
