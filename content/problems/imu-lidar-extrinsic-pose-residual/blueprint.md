---
{
  "schema_version": 1,
  "problem_id": "imu-lidar-extrinsic-pose-residual",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Assemble an IMU-Lidar Pose Constraint",
  "summary": "`imu_lidar_residual(world_from_imu, imu_from_lidar, lidar_relative, std)` world_from_imu(2,4,4),sharedextrinsic(4,4),lidar_relative(4,4) maps lidar-j into lidar-i;std(6)in[1e-6,1000], translationmeters thenrotationradians. Predicted lidarrelative=(Ti Til)^-1(Tj Til). E=lidar_relative^-1 predicted. Return predicted(4,4),translation=E[:3,3] with shape (3,),rotation=Log(E.R)(3),whitened(6)=concattranslation,rotation/std,costhalf norm\u00b2. Requireprincipalrotationerror<=pi\u22121e-4. Translation is in measured residual frame; split translation/rotation residual is explicitly NOT full SE3Log translational Jacobian or complete LIO-SAM IMU velocity/bias factor. ExampleextrinsicI,posesI andtranslationx2,measuredtranslationx1,std1=>translation[1,0,0],rotation0,cost.5. ExamplepureIMURz90 with lidarleverarm[1,0,0]=>predictedRz90,translation[-1,1,0],matchingmeasurement giveszero. Knownextrinsics are essential.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "lio-sam"
  ],
  "paper_ids": [
    "2020-lio-sam"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2020-lio-sam"
  ],
  "prerequisite_problem_ids": [
    "compose-frame-transforms",
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
  "entrypoint": "solution.imu_lidar_residual",
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
    "evaluator_sha256": "77115f07016bece11ee52171b9125b00cf2a35299a37ac0e7aa3567bf9113a52"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2007.00258"
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

# Assemble an IMU-Lidar Pose Constraint

Implement `imu_lidar_residual(world_from_imu, imu_from_lidar, lidar_relative, std)`.

`imu_lidar_residual(world_from_imu, imu_from_lidar, lidar_relative, std)` world_from_imu(2,4,4),shared extrinsic(4,4),lidar_relative(4,4) maps lidar-j into lidar-i;std(6)in[1e-6,1000], translation meters thenrotation radians.

Predicted lidar relative=(Ti Til)^-1(Tj Til). E=lidar_relative^-1 predicted.

Return predicted(4,4),translation=E[:3,3] with shape (3,),rotation=Log(E.R)(3),whitened(6)=concattranslation,rotation/std,cost half norm².

Requireprincipal rotation error<=pi−1e-4.

Translation is in measured residual frame; split translation/rotation residual is explicitly NOT full SE(3) log translational Jacobian or complete LIO-SAM IMU velocity/bias factor.

Example: extrinsic I,posesI andtranslationx2,measuredtranslationx1,std1=>translation[1,0,0],rotation0,cost.5.

Example: pure IMU Rz90 with lidar lever arm[1,0,0]=>predictedRz90,translation[-1,1,0],matching measurement gives zero.

Known extrinsics are essential.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity extrinsic, IMU world poses at x=0 and x=2, measured lidar relative translation x=1, and all standard deviations 1 give translation residual [1,0,0], zero rotation residual, and cost 0.5.
2. The IMU rotates 90 degrees about z at a fixed origin. A lidar mounted one meter along IMU x has relative rotation Rz90 and relative translation [-1,1,0].

Supplying exactly that measurement gives zero cost.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.00258).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compose endpoint lidar poses, invert the first rigidly, then compare with the supplied measurement.

Rotation logarithm uses stable small-angle and near-pi conventions.

Fixed-size inputs give constant time/storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected.

Independent review precedes publication.
