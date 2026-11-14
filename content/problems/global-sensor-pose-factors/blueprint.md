---
{
  "schema_version": 1,
  "problem_id": "global-sensor-pose-factors",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Assemble Sensor-Specific Pose Factors",
  "summary": "`global_factors(world_from_body, body_from_sensor, gps, magnetic, world_field, height, std, valid)` transforms(N,4,4) and shared(4,4),0<=N<=4096. Sensor offset/rotation known; one collocated GPS/magnetometer/barometer frame is a teaching restriction. GPS(N,3) world ENU meters, magnetic(N,3) sensor-frame field vector in microtesla, world_field(3) ENU same units. Require each magnetic norm and world_field norm>1e-9 including masked rows. Height(N) is sensor altitude meters in same ENU datum (pressure conversion already done). std(N,7) in[1e-6,1000], ordered3 GPS meters,3 unit-direction dimensionless,1 height meters; valid(N,3) GPS/magnetic/barometer availability. Predicted sensor pose Ts=Tb Tbs. Residual signs measured-minus-predicted: gps-p_s, magnetic/norm\u2212R_s.T(world_field/norm), height-p_s,z. Return raw(N,7),whitened(N,7),cost Pythonfloat .5sum(whitened\u00b2); unavailable entire sensor block zero, all supplied values still validated. Whitening uses diagonal std, not full covariance. No calibrated field magnitude heuristic or bias estimation. Example allidentity, gps[1,2,3],mag[1,0,0],worldfield[1,0,0],height4,std1,allvalid=>raw[1,2,3,0,0,0,4],cost15. Examplebodyidentity, sensor offset[1,0,0],sensorrotationRz90, gps[1,0,0],mag[0,-2,0],field[5,0,0],height0=>allzero.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "vins-fusion"
  ],
  "paper_ids": [
    "2019-vins-fusion"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2019-vins-fusion"
  ],
  "prerequisite_problem_ids": [
    "compose-frame-transforms"
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
  "entrypoint": "solution.global_factors",
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
    "evaluator_sha256": "dadf30295b504c994cc1c604fb8f841ef4d552c3c48114e4bc550a6733267897"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1901.03642"
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

# Assemble Sensor-Specific Pose Factors

Implement `global_factors(world_from_body, body_from_sensor, gps, magnetic, world_field, height, std, valid)`.

`global_factors(world_from_body, body_from_sensor, gps, magnetic, world_field, height, std, valid)` transforms(N,4,4) and shared(4,4),0<=N<=4096.

Sensor offset/rotation known; one collocated GPS/magnetometer/barometer frame is a teaching restriction.

GPS(N,3) world ENU meters, magnetic(N,3) sensor-frame field vector in microtesla, world_field(3) ENU same units.

Require each magnetic norm and world_field norm>1e-9 including masked rows.

Height(N) is sensor altitude meters in same ENU datum (pressure conversion already done). std (N,7) in[1e-6,1000], ordered3 GPS meters,3 unit-direction dimensionless,1 height meters; valid(N,3) GPS/magnetic/barometer availability.

Predicted sensor pose Ts=Tb Tbs.

Residual signs measured-minus-predicted: gps-p_s, magnetic/norm−R_s.T(world_field/norm), height-p_s,z.

Return raw(N,7),whitened(N,7),cost Python float .5sum(whitened²); unavailable entire sensor block zero, all supplied values still validated.

Whitening uses diagonal std, not full covariance.

No calibrated field magnitude heuristic or bias estimation.

Example all identity, gps[1,2,3],mag[1,0,0],world field[1,0,0],height4,std1,all valid=>raw[1,2,3,0,0,0,4],cost15.

Example: body identity, sensor offset[1,0,0],sensor rotationRz90, gps[1,0,0],mag[0,-2,0],field[5,0,0],height0=>all zero.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Body and sensor transforms are identity.

GPS [1,2,3], magnetic [1,0,0], world field [1,0,0], height 4, all standard deviations 1 and all sensors available give raw [1,2,3,0,0,0,4] and cost 15.
2. The body is identity; the sensor has translation [1,0,0] and a 90-degree z rotation.

GPS [1,0,0], sensor magnetic [0,-2,0], world field [5,0,0], and height 0 give zero residuals.

## Source and scope

[Primary source](https://arxiv.org/abs/1901.03642).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compose sensor poses, construct the three models, mask by sensor and divide by matching standard deviations.

Time/storage O(N).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected.

Independent review precedes publication.
