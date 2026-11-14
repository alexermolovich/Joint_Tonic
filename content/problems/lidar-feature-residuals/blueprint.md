---
{
  "schema_version": 1,
  "problem_id": "lidar-feature-residuals",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Compute Point-to-Line and Point-to-Plane Scan Residuals",
  "summary": "Compute signed point-to-plane and unsigned point-to-line residuals after transforming scan features into the map frame.",
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
    "2020-lio-sam",
    "2021-fast-lio-2"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2020-lio-sam"
  ],
  "prerequisite_problem_ids": [
    "se3-transform-points"
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
  "entrypoint": "solution.scan_residuals",
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
    "evaluator_sha256": "9a8f1e29748c9ab00527dd8631b86ee9a68ea158c4a503d97abd47850f9ba4d2"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2007.00258",
      "https://arxiv.org/abs/2107.06829"
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

# Compute Point-to-Line and Point-to-Plane Scan Residuals

Implement `scan_residuals(plane_points, plane_anchors, plane_normals, line_points, line_a, line_b, world_from_lidar)`.

Compute signed point-to-plane and unsigned point-to-line residuals after transforming scan features into the map frame.

`plane_points`, `plane_anchors`, `plane_normals` are float64 `(P,3)`; `line_points`, `line_a`, `line_b` are float64 `(L,3)`; `0<=P,L<=8192`. Scan points are in one synchronized lidar frame; plane anchors/normals and line endpoints are in a common world/map frame. Points and translations use meters. `world_from_lidar` is a proper float64 `(4,4)` rigid transform, validated with atol=1e-9, rtol=0 for its rotation and last row.

Every plane normal must have norm within `1e-9` of one; normalize accepted normals. Every line's endpoints must be separated by at least `1e-6` meters. Transform each scan point to the world frame. Return a dictionary with fresh float64 `plane (P,) = normal dot (world_point-plane_anchor)` and `line (L,) = norm(cross(world_point-line_a,line_b-line_a))/norm(line_b-line_a)`, both in meters. Plane sign follows the supplied normal; line distances are nonnegative. Empty groups are allowed. No nearest-neighbor association, robust loss, filtering or pose update is performed. This one package supplies both the FAST-LIO2 point-to-plane kernel and LIO-SAM-style line/plane feature residual practice.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With identity transform, plane scan point `[[0.,0.,2.]]`, anchor `[[0.,0.,0.]]` and normal `[[0.,0.,1.]]`, the signed plane residual is `[2.]` meters. Line scan point `[[0.,1.,0.]]`, endpoints `[[0.,0.,0.]]` and `[[2.,0.,0.]]` give line distance `[1.]` meter.
2. Keep the plane point and anchor but negate the normal: plane residual is `[-2.]`. Reversing a line's endpoint order leaves its nonnegative distance unchanged.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.00258). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Validate the shared transform and each feature geometry, transform scan points once, then compute normal projections and perpendicular line distances. O(P+L) time and memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
