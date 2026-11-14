---
{
  "schema_version": 1,
  "problem_id": "short-window-imu-preintegration",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Preintegrate a Short IMU Window",
  "summary": "Integrate one synchronized window of angular velocity and specific force in its initial body frame.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "vins-mono"
  ],
  "paper_ids": [
    "2017-vins-mono"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2017-vins-mono"
  ],
  "prerequisite_problem_ids": [
    "integrate-imu-rotation",
    "preintegrate-imu-translation"
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
  "entrypoint": "solution.preintegrate_window",
  "physical_contract": {
    "frames": [
      "Explicit world, body, camera or dimensionless scaled-state frame in the contract"
    ],
    "units": {
      "values": "Meters, seconds, radians, pixels, or dimensionless normalized quantities as defined per argument"
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
    "evaluator_sha256": "92c5ed836086a8d86a2bf6197bddbb7fba345d50149761f3d31c68126541c336"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1708.03852"
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

# Preintegrate a Short IMU Window

Implement `preintegrate_window(angular_velocity, specific_force, gyro_bias, accel_bias, durations)`.

Integrate one synchronized window of angular velocity and specific force in its initial body frame.

`angular_velocity (N,3)` and `specific_force (N,3)` are float64 in radians/second and meters/second squared. `gyro_bias (3,)` and `accel_bias (3,)` use the same respective units. All these entries have absolute magnitude <=100; `0<=N<=4096`. `durations (N,)` is float64 seconds, each in `[1e-6,1]`, total <=100 seconds. Each sample describes constant measurements over its interval, and biases remain constant over the window.

Initialize relative rotation R=I, velocity increment v=0 and position increment p=0. From the OLD R,v,p in each interval compute p_next=p+v*dt+0.5*R@(force-accel_bias)*dt^2; v_next=v+R@(force-accel_bias)*dt; R_next=R@Exp((angular_velocity-gyro_bias)*dt). Use a continuous small-angle SO(3) exponential.

Return `rotations (N+1,3,3)`, `velocity (N+1,3)`, `position (N+1,3)` and `elapsed (N+1,)`, including initial identity/zeros. R maps the current body frame into the initial body frame; v,p are increments expressed in that initial frame, in m/s and m. Gravity is deliberately excluded. This original zero-order-hold recurrence composes rotation and translation integration; it is not midpoint integration, covariance/bias-Jacobian propagation, or the complete VINS-Mono preintegrator.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One zero-angular-rate sample with specific force `[2.,0.,0.]`, zero biases and duration 0.1 s gives final velocity `[0.2,0.,0.]` m/s, position `[0.01,0.,0.]` m and identity rotation.
2. Two one-second intervals with body angular rate `[0.,0.,pi/2]` and body specific force `[1.,0.,0.]` each give final rotation Rz(pi), velocity `[1.,1.,0.]` m/s and position `[1.5,0.5,0.]` m. The second force is rotated by the interval's starting orientation.

## Source and scope

[Primary source](https://arxiv.org/abs/1708.03852). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Keep old orientation and velocity until both translation updates are formed, then apply the angular increment on the right. O(N) time and O(N) returned history storage. Internal state is constant-sized.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
