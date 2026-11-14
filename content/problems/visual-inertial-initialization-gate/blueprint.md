---
{
  "schema_version": 1,
  "problem_id": "visual-inertial-initialization-gate",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Validate a Visual-Inertial Initialization",
  "summary": "`validate_initialization(scale, gravity, gyro_bias, accel_bias, residuals, valid, jacobian, limits)` scale builtinfloat/int[1e-6,1e3];gravity3worldm/s\u00b2,gyro_bias3rad/s,accel_bias3m/s\u00b2;residuals(R)alreadywhiteneddimensionless,valid(R)bool,R0..4096;jacobian(R,D)dimensionless whitened/scaled gauge-fixed,1<=D<=32,abs<=1000;limits(7)floats = [min_scale,max_scale,gravity_tolerance,max_gyro_norm,max_accel_norm,max_rms,relative_rank_cutoff], scaleintervalwithin[1e-6,1e3]ordered, otherthresholds[0,1000], cutoff[1e-12,.01]. Eligible rowsvalid determine RMSandSVD rank strict sigma>cut*sigma_max. Return countint,rankint,rmsfloat(NaNifnone),gravity_errorfloat abs(normgravity\u22129.81),checks bool(6) ordered [atleastDvalidrows AND rankD, minscale<=scale<=maxscale, gravityerror<=tol, gyronorm<=max,accelnorm<=max,rms<=max],acceptedbool(allchecks). No-evidence RMScheckFalse. Original inspectable diagnostic over supplied initialization candidate, not optimizer, ORB-SLAM3 exact acceptanceheuristic, or nonlinearobservability proof. Gravity directionnotgated: estimateisworldframe and onlymagnitudecheck. ExampleD1,R1,J[[1]],residual[.2],validTrue,scale1,g[0,0,-9.81],biases0,limits[.5,2,.1,.1,.1,.2,1e-6]=>allTrue,rms.2,rank1. ExampletwoidenticalJrows[[1,0],[1,0]],residual0=>rank1,firstFalse,rejectevenperfectfit.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "orb-slam-3"
  ],
  "paper_ids": [
    "2020-orb-slam-3"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2020-orb-slam-3"
  ],
  "prerequisite_problem_ids": [
    "initialization-observability-rank"
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
  "entrypoint": "solution.validate_initialization",
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
    "evaluator_sha256": "ebcd2c3d4afac0549f75c126081594ed3967f14214fa8d664961b4b98447027a"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2007.11898"
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

# Validate a Visual-Inertial Initialization

Implement `validate_initialization(scale, gravity, gyro_bias, accel_bias, residuals, valid, jacobian, limits)`.

`validate_initialization(scale, gravity, gyro_bias, accel_bias, residuals, valid, jacobian, limits)` scale builtinfloat/int[1e-6,1e3];gravity3world m/s²,gyro_bias (3,)rad/s,accel_bias (3,)m/s²;residuals(R)already whitened dimensionless,valid(R)bool,R0..4096;jacobian(R,D)dimensionless whitened/scaled gauge-fixed,1<=D<=32,abs<=1000;limits(7)floats = [min_scale,max_scale,gravity_tolerance,max_gyro_norm,max_accel_norm,max_rms,relative_rank_cutoff], scale interval within[1e-6,1e3]ordered, other thresholds[0,1000], cutoff[1e-12,.01].

Eligible rowsvalid determine RMS and SVD rank with strict cutoff sigma>cut*sigma_max.

Return count int,rank int,rms float(NaN if none),gravity_error float abs(normgravity−9.81),checks bool(6) ordered [at least D valid rows AND rank D, minscale<=scale<=maxscale, gravity error<=tol, gyro norm<=max,accelerometer norm<=max,RMS <=max],acceptedbool(allchecks).

No-evidence RMS check is False.

Original inspectable diagnostic over supplied initialization candidate, not optimizer, ORB-SLAM3 exact acceptanceheuristic, or nonlinearobservability proof.

Gravity directionnotgated: estimateisworld frame and only magnitude check.

Example: D=1,R1,J[[1]],residual[.2],validTrue,scale1,g[0,0,-9.81],biases0,limits[.5,2,.1,.1,.1,.2,1e-6]=>all True,rms.2,rank1.

Example: two identical J rows[[1,0],[1,0]],residual0=>rank1,first False,reject even a perfect fit.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Scale 1, gravity [0,0,-9.81], zero biases, residual [0.2], valid [True], Jacobian [[1]], and limits [0.5,2,0.1,0.1,0.1,0.2,1e-6] pass all six checks.

Rank is 1 and RMS is 0.2.
2. Jacobian rows [[1,0],[1,0]] have rank 1 despite two observations and zero residuals.

The observability check fails, so the candidate is rejected even with a perfect residual fit.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.11898).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Apply the valid-row mask consistently to residual RMS and the scaled Jacobian SVD, then compute independent physical checks.

Time O(RD²), storage O(RD), with D at most 32.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected.

Independent review precedes publication.
