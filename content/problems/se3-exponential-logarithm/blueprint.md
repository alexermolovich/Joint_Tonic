---
{
  "schema_version": 1,
  "problem_id": "se3-exponential-logarithm",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Apply SE(3) Exponential and Logarithm Maps",
  "summary": "Compute an SE(3) exponential and principal logarithm with explicit translation/rotation coupling.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "micro-lie-theory"
  ],
  "paper_ids": [
    "2018-micro-lie-theory"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2018-micro-lie-theory"
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
  "entrypoint": "solution.se3_maps",
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
    "evaluator_sha256": "4e8136d1f36124e7120d2d74b287433fe6eea024e15ed0e692a8922bf94edfdd"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1812.01537"
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

# Apply SE(3) Exponential and Logarithm Maps

Implement `se3_maps(tangent, transform)`.

Compute an SE(3) exponential and principal logarithm with explicit translation/rotation coupling.

`tangent` is float64 `(6,)`, ordered `[rho_x,rho_y,rho_z,phi_x,phi_y,phi_z]`. Rho is a translation tangent in meters, with norm<=1e6; phi is a rotation vector in radians, with norm<=pi-1e-4. `transform` is a proper float64 `(4,4)` rigid transform with translation in meters and principal rotation angle<=pi-1e-4. Validate rotation and homogeneous row at atol=1e-9, rtol=0. The two inputs are independent: neither must be the map of the other.

Return a dictionary with fresh float64 `exponential (4,4)=Exp(tangent)` and `logarithm (6,)=Log(transform)`. Write Omega=skew(phi), theta=norm(phi). Rotation is `I+(sin(theta)/theta)*Omega+((1-cos(theta))/theta**2)*Omega**2`. The translation is `V@rho`, where `V=I+((1-cos(theta))/theta**2)*Omega+((theta-sin(theta))/theta**3)*Omega**2`. Use continuous series limits at zero. For Log, recover the principal rotation vector, build its V, then solve `V@rho=translation`.

These right-handed maps define an increment; no pose composition, left/right update or interpolation is performed. The ambiguous pi branch and its immediate 1e-4-radian neighborhood are outside this bounded contract. Translation is generally not equal to rho when rotation is nonzero.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Tangent `[1.,0.,0.,0.,0.,0.]` and identity transform yield an exponential that translates one meter along x, and a zero logarithm.
2. Tangent `[1.,0.,0.,0.,0.,pi/2]` yields a 90-degree z rotation with translation `[2/pi,2/pi,0]`, not `[1,0,0]`. Supplying this resulting transform to Log recovers the same six-vector.

## Source and scope

[Primary source](https://arxiv.org/abs/1812.01537). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Use stable scalar series near zero, construct Rodrigues rotation and V, and solve the translation part of the logarithm. Recover angle using atan2 of skew magnitude and trace-derived cosine to remain stable near the supported upper branch. Constant-size O(1) time and memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
