---
{
  "schema_version": 1,
  "problem_id": "preintegrate-imu-translation",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Preintegrate Bias-Corrected IMU Velocity and Position",
  "summary": "Preintegrate accelerometer velocity and position increments in the initial keyframe body frame.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "on-manifold-preintegration"
  ],
  "paper_ids": [
    "2015-on-manifold-preintegration"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2015-on-manifold-preintegration"
  ],
  "prerequisite_problem_ids": [
    "integrate-imu-rotation"
  ],
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
  "entrypoint": "solution.preintegrate_translation",
  "physical_contract": {
    "frames": [
      "Right-handed camera, lidar, world or initial IMU frame as explicitly defined"
    ],
    "units": {
      "values": "Meters, radians, seconds, pixels and declared derivatives; intensity dimensionless"
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
      "Independent mechanism checks",
      "Boundary and invalid inputs",
      "Input preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "5c642e2a14880d01ff80d14dc80077aefd4801656318b31b6013e6e9955ef2d9"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1512.02363"
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

# Preintegrate Bias-Corrected IMU Velocity and Position

Implement `preintegrate_translation(accelerations, accelerometer_bias, relative_rotations, durations)`.

Preintegrate accelerometer velocity and position increments in the initial keyframe body frame.

`accelerations` is float64 `(N,3)` specific force in m/s², `accelerometer_bias` float64 `(3,)` in m/s², with absolute entries<=100. `relative_rotations` is float64 `(N,3,3)`, each a proper rotation mapping sample k's body frame into the initial keyframe frame at the START of interval k. Validate rotations with atol=1e-9, rtol=0. `durations` is float64 `(N,)` seconds in `[1e-6,1]` with total<=100; `0<=N<=4096`.

Initialize velocity and position increments to zero. At each interval compute `force=relative_rotations[k]@(accelerations[k]-accelerometer_bias)`. Update position using the OLD velocity: `position_next=position+velocity*dt+0.5*force*dt**2`; then `velocity_next=velocity+force*dt`. Return fresh float64 `velocity (N+1,3)`, `position (N+1,3)` and `elapsed (N+1,)`, including the initial zeros, in a dictionary. Velocity and position use m/s and meters in the initial body frame.

Gravity is deliberately absent from these preintegrated quantities; it is restored when forming a world-state factor. Supplied specific force is not assumed to be zero for a stationary physical accelerometer. Rotation integration, covariance and extrinsic estimation are outside this component. Empty samples return one zero state.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One specific-force sample `[[2.,0.,0.]]`, zero bias, identity interval-start rotation, duration `[0.1]` produce final velocity `[0.2,0.,0.]` m/s and position `[0.01,0.,0.]` meters.
2. Two identical samples and durations give final velocity `[0.4,0.,0.]` m/s and position `[0.04,0.,0.]` meters. Both output traces include their initial zero row.

## Source and scope

[Primary source](https://arxiv.org/abs/1512.02363). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Rotate corrected specific force into the initial frame once per interval. Compute position from old velocity, then update velocity, retaining the full trace. O(N) time and output memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
