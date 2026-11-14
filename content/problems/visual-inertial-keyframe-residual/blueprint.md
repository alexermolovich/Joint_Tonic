---
{
  "schema_version": 1,
  "problem_id": "visual-inertial-keyframe-residual",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Build a Visual-Inertial Residual",
  "summary": "Combine a keyframe IMU residual with already computed visual residuals using declared diagonal uncertainties.",
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
    "short-window-imu-preintegration",
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
  "entrypoint": "solution.keyframe_residual",
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
    "evaluator_sha256": "bdca13b735749f2ed0ac4204fbd0352fbb74381510dc172992d3fb0e1b128d4f"
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

# Build a Visual-Inertial Residual

Implement `keyframe_residual(rotations, positions, velocities, gravity, duration, delta_rotation, delta_velocity, delta_position, imu_std, visual_residuals, visual_std)`.

Combine a keyframe IMU residual with already computed visual residuals using declared diagonal uncertainties.

`rotations (2,3,3)` are proper float64 body-to-world rotations at keyframes i,j. `positions (2,3)` and `velocities (2,3)` are world-frame meters and m/s. `gravity (3,)` is world-frame m/s squared, absolute entries <=100. `duration` is a Python int/float in `[1e-6,100]` seconds. `delta_rotation (3,3)` is proper, and `delta_velocity (3,)`, `delta_position (3,)` are preintegrated increments in the initial body frame, in m/s and m.

`imu_std (9,)` is float64 in `[1e-6,1000]`, ordered rotation (radians), velocity (m/s), position (m). `visual_residuals (N,2)` and `visual_std (N,2)` are float64 pixel quantities, `0<=N<=16384`, std entries in `[1e-6,1000]`. Visual residuals are supplied measured-minus-projected pixels; projection is outside this function.

Compute rR=Log(delta_rotation.T@Ri.T@Rj), the principal SO(3) rotation vector, requiring its angle <=pi-1e-4. Compute rv=Ri.T@(vj-vi-gravity*T)-delta_velocity, and rp=Ri.T@(pj-pi-vi*T-0.5*gravity*T^2)-delta_position. Return `inertial (9,)` ordered rR,rv,rp; `whitened (9+2N,)` comprising inertial/imu_std followed by flattened visual_residuals/visual_std in row-major order; and Python float `cost=0.5*dot(whitened,whitened)`.

All proper rotations use atol=1e-9, rtol=0 validation. This is a diagonal-noise teaching factor without bias-state residuals, full covariance whitening, robust visual loss or optimization. Do not add gravity to the supplied preintegrated increments.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity orientations, zero positions/velocities, gravity `[0.,0.,-10.]`, T=0.1 s, delta_velocity `[0.,0.,1.]`, delta_position `[0.,0.,0.05]` and identity delta_rotation give zero IMU residual: gravity and stationary specific-force increments cancel.
2. Gravity zero, identity rotations, zero velocities/increments, positions i=`[0.,0.,0.]`, j=`[1.,0.,0.]`, T=1 s, all standard deviations 1 and visual residual `[[3.,4.]]` give rp=`[1.,0.,0.]` and cost `(1+9+16)/2=13`.

## Source and scope

[Primary source](https://arxiv.org/abs/1708.03852). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute the relative rotation error and initial-frame translation residuals, then concatenate independently whitened blocks. O(N) time and memory for N supplied visual observations.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
