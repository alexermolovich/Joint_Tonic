---
{
  "schema_version": 1,
  "problem_id": "integrate-imu-rotation",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Integrate IMU Rotation Increments on SO3",
  "summary": "Integrate bias-corrected body angular velocities with right-multiplied SO(3) increments.",
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
    "se3-exponential-logarithm"
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
  "entrypoint": "solution.integrate_imu_rotation",
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
    "evaluator_sha256": "8085e3aa974d16c19cc467182062d1b5084cb4043e9d4b55bf92194b56acd969"
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

# Integrate IMU Rotation Increments on SO3

Implement `integrate_imu_rotation(angular_velocity, gyro_bias, durations)`.

Integrate bias-corrected body angular velocities with right-multiplied SO(3) increments.

`angular_velocity` is float64 `(N,3)` rad/s, `gyro_bias` float64 `(3,)` rad/s, both with absolute entries<=100. `durations` is float64 `(N,)` seconds, each in `[1e-6,1]`, total<=100; `0<=N<=4096`. Samples are chronological and each rate/bias describes that sample's right-handed body frame. The constant bias uses the same sensor-axis convention across the window.

Initialize DeltaR=I. For sample k compute rotation vector `(angular_velocity[k]-gyro_bias)*durations[k]`, apply the Rodrigues exponential with stable zero-angle limits, then update `DeltaR_next=DeltaR @ Exp(vector)` in that order. Return a dictionary with fresh float64 `rotations (N+1,3,3)` including initial identity, and `elapsed (N+1,)` containing zero followed by cumulative durations. Rotation k maps body-frame vectors at that state into the initial keyframe body coordinates. Empty input returns one identity and elapsed `[0.]`. No Euler-angle addition, gravity, velocity, covariance or bias estimation is included.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Angular velocity `[[0.,0.,pi/2]]`, zero gyro bias, duration `[1.]` produce initial identity followed by a 90-degree z rotation, elapsed `[0.,1.]`.
2. Angular velocities equal to the supplied gyro bias produce identity at every state. An empty window also returns identity and zero elapsed time.

## Source and scope

[Primary source](https://arxiv.org/abs/1512.02363). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Subtract the fixed bias, form each interval rotation vector, and right-multiply its exponential onto the previous orientation. Preserve every intermediate matrix so downstream preintegration can use interval-start rotations. O(N) time and memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
