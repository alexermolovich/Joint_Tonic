---
{
  "schema_version": 1,
  "problem_id": "velocity-acceleration-command-limits",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Enforce Velocity and Acceleration Limits",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.limit_joint_commands",
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
      "robot joint coordinates"
    ],
    "units": {
      "positions,targets": "radians",
      "velocities": "radians/second",
      "acceleration": "radians/second\u00b2",
      "dt": "seconds"
    },
    "axes": "Independent signed joint axes; no wrapping.",
    "timestamp_assumptions": "Each target is requested at the end of one fixed positive dt interval.",
    "batching": "initial_position/velocity(D,), targets(T,D), max_velocity/acceleration(D,) -> float64 positions(T,D), velocities(T,D)."
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
    "evaluator_sha256": "c55d8a906f58c86e2b324420b12f062d03afb8df49e2994f593071d39753eb30"
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
  "summary": "Generate joint commands by projecting requested velocities into velocity and acceleration limits.",
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

# Enforce Velocity and Acceleration Limits

Generate joint commands by projecting requested velocities into velocity and acceleration limits.

```python
def limit_joint_commands(initial_position, initial_velocity, targets, dt, max_velocity, max_acceleration):
```

## Contract

D>=1. dt is positive scalar; per-joint velocity and acceleration limits are positive. Initial velocity must satisfy its limits. At each step compute desired_velocity=(target-current_position)/dt. Clip to intersection [-max_velocity,max_velocity] and [previous_velocity-max_acceleration*dt,previous_velocity+max_acceleration*dt], then advance position by clipped_velocity*dt. Empty targets (0,D) produce empty outputs. Targets need not be reached; no joint position or collision constraints are enforced.

**Shapes and outputs:** initial_position/velocity(D,), targets(T,D), max_velocity/acceleration(D,) -> float64 positions(T,D), velocities(T,D).

**Units:** positions,targets: radians, velocities: radians/second, acceleration: radians/secondÂ², dt: seconds. **Time:** Each target is requested at the end of one fixed positive dt interval.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `initial_position=[0], initial_velocity=[0], targets=[[10],[10],[10]], dt=1, max_velocity=[2], max_acceleration=[1]` â†’ positions `[[1],[3],[5]]`, velocities `[[1],[2],[2]]`.
2. `initial_position=[0], initial_velocity=[2], targets=[[-10]], dt=1, max_velocity=[2], max_acceleration=[1]` â†’ position `[[1]]`, velocity `[[1]]`; braking cannot reverse velocity instantly.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

dt must be at least 1e-9 seconds; smaller values raise ValueError.
