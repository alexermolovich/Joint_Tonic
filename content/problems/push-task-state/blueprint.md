---
{
  "schema_version": 1,
  "problem_id": "push-task-state",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Push Robot State into a Task Space",
  "summary": "Push a synchronized joint velocity through a supplied task Jacobian.",
  "type": "component",
  "difficulty": "easy",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "rmpflow"
  ],
  "paper_ids": [
    "2018-rmpflow"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2018-rmpflow"
  ],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.push_task_state",
  "physical_contract": {
    "frames": [
      "Declared joint coordinates or a common right-handed world frame, as specified"
    ],
    "units": {
      "values": "Radians, seconds, meters and corresponding derivatives; normalized spaces explicitly identified"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent numerical mechanism",
      "Boundary and malformed inputs",
      "Noncontiguous realistic scale and preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "e90d95b390964e4bafcc8d4cbbafd32c51b6eca31a1a5b807374e2bc14057c43"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1811.07049"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Push Robot State into a Task Space

Implement `push_task_state(task_position, jacobian, joint_velocity)`.

Push a synchronized joint velocity through a supplied task Jacobian.

`task_position` is float64 `(T,)` meters, `1<=T<=16`. `jacobian` is float64 `(T,D)` meters/radian, `1<=D<=16`. `joint_velocity` is float64 `(D,)` radians/second. The caller has evaluated the task map and Jacobian at the same joint configuration and time; task axes retain that map's ordering in its declared frame. Return a dictionary containing fresh float64 `position (T,)`, a copy of task_position, and `velocity (T,) = jacobian @ joint_velocity` in meters/second. This is one RMP pushforward operation; no forward kinematics, finite-difference Jacobian, automatic differentiation or acceleration calculation is requested.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Position `[3.,4.]`, Jacobian `[[1.,2.],[0.,1.]]`, joint velocity `[2.,-1.]` give position `[3.,4.]` and task velocity `[0.,-1.]` m/s.
2. Position `[1.]`, Jacobian `[[2.,3.]]`, joint velocity `[0.,0.]` give position `[1.]` and velocity `[0.]`, both in fresh arrays.

## Source and scope

[Primary source](https://arxiv.org/abs/1811.07049). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Copy the supplied position and multiply the Jacobian by the velocity in the documented axis order. O(TD) time and O(T) output memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
