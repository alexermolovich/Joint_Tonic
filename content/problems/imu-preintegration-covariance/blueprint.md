---
{
  "schema_version": 1,
  "problem_id": "imu-preintegration-covariance",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Propagate Preintegration Covariance",
  "summary": "`preintegration_covariance(rotation_vectors, specific_force, durations, noise_variance)` rotation_vectors(N,3) body-frame integrated angular increments radians, norm<=3; force(N,3) bias-corrected body specificforce m/s\u00b2 abs<=100;dt(N)seconds[1e-6,1],sum<=100,N0..1024;noise_variance(N,6) in[0,100], per-sample discrete variances of gyroscope(rad/s) then accelerometer(m/s\u00b2), NOT continuous spectral densities. Start rotation R=I,cov P=zeros9. State error order(theta radians,velocity m/s,position m), theta right-local current-body, velocity/position initialbody. For eachOLD R and h=dt, phi=rotvec, E=Exp(phi), rightJacobian Jr=I\u2212(1\u2212cos\u03b8)/\u03b8\u00b2[phi]x+(\u03b8\u2212sin\u03b8)/\u03b8\u00b3[phi]x\u00b2 with analytic small-angle continuation. A block rows [[E.T,0,0],[-R[f]x h,I,0],[-.5R[f]x h\u00b2,I h,I]]. B block rows [[Jr h,0],[0,R h],[0,.5R h\u00b2]]. P'=A P A.T+B diag(q) B.T, symmetrize roundoff; R'=R E. Return covariance(N+1,9,9) and final_rotation(3,3). This reproduces the nine-state first-order noise recurrence with supplied increments, fixed biases, and diagonal discrete sensor noise; no bias random walk or continuous-noise discretization. Exampleonezero-rotation/force step h1,qgyro1,qaccel4=>diagtheta1,diagv4,diagp1 and each matching v/p covariance2. ExampleN0=>singlezero9matrix,Ridentity. Independent oracle propagates noise impulse columns through the error recurrence before forming their Gram matrix.",
  "type": "component",
  "difficulty": "hard",
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
  "entrypoint": "solution.preintegration_covariance",
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
    "evaluator_sha256": "32922d08fd059d8a3d398ea049d1960ee5db885af931100f515064bccb702a6c"
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

# Propagate Preintegration Covariance

Implement `preintegration_covariance(rotation_vectors, specific_force, durations, noise_variance)`.

`preintegration_covariance(rotation_vectors, specific_force, durations, noise_variance)` rotation_vectors (N,3) body-frame integrated angular increments radians, norm<=3; force(N,3) bias-corrected body specific force m/s² abs<=100;dt(N)seconds[1e-6,1],sum<=100,N0..1024;noise_variance (N,6) in[0,100], per-sample discrete variances of gyroscope(rad/s) then accelerometer(m/s²), NOT continuous spectral densities.

Start rotation R=I,cov P=zeros9.

State error order(theta radians,velocity m/s,position m), theta right-local current-body, velocity/position initial body.

For each old R and h=dt, phi=rotvec, E=Exp(phi), right Jacobian Jr=I−(1−cosθ)/θ²[phi]x+(θ−sinθ)/θ³[phi]x² with analytic small-angle continuation. A block rows [[E.T,0,0],[-R[f]x h,I,0],[-.5R[f]x h²,I h,I]]. B block rows [[Jr h,0],[0,R h],[0,.5R h²]]. P'=A P A.T+B diag(q) B.T, symmetrize roundoff; R'=R E.

Return covariance(N+1,9,9) and final_rotation(3,3).

This reproduces the nine-state first-order noise recurrence with supplied increments, fixed biases, and diagonal discrete sensor noise; no bias random walk or continuous-noise discretization.

Example: one zero-rotation/force step h1,gyro variances 1,accelerometer variances 4=>diagonal orientation variances 1,diagonal velocity variances 4,diagonal position variances 1 and each matching v/p covariance2.

Example: N=0=>single zero 9×9 matrix,R identity.

Independent oracle propagates noise impulse columns through the error recurrence before forming their Gram matrix.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One sample has zero rotation and force, duration 1 second, gyro variances [1,1,1] and accelerometer variances [4,4,4].

Final orientation-error variances are 1, velocity variances 4, position variances 1, and matching velocity/position cross-covariances 2.
2. Empty sample arrays return covariance shape (1,9,9) containing zeros and final rotation equal to identity.

## Source and scope

[Primary source](https://arxiv.org/abs/1512.02363).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Build the nine-state transition and six-noise injection at every sample, then propagate the full covariance.

Constant-size matrices give O(N) time and O(N) trace storage.

The right Jacobian needs a small-angle series.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected.

Independent review precedes publication.
