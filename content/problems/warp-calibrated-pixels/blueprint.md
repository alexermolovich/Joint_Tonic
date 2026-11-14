---
{
  "schema_version": 1,
  "problem_id": "warp-calibrated-pixels",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Warp a Point Between Calibrated Frames",
  "summary": "Unproject source pixels, transform their depth hypotheses, and project them into a target camera.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "direct-sparse-odometry"
  ],
  "paper_ids": [
    "2016-direct-sparse-odometry"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2016-direct-sparse-odometry"
  ],
  "prerequisite_problem_ids": [
    "project-camera-points",
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
  "entrypoint": "solution.warp_pixels",
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
    "evaluator_sha256": "05e9d8b9eaeaf90974890a67613761a16284f9b08999ce3d74173c03d65059a5"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1607.02565"
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

# Warp a Point Between Calibrated Frames

Implement `warp_pixels(pixels, inverse_depth, source_intrinsics, target_intrinsics, target_from_source, target_size)`.

Unproject source pixels, transform their depth hypotheses, and project them into a target camera.

`pixels` is float64 `(N,2)` in `(x,y)` pixel order; `inverse_depth` is float64 `(N,)` in `[1e-6,1e6]` inverse meters; `0<=N<=16384`. Source and target intrinsics are float64 `(4,)` ordered `[fx,fy,cx,cy]`, with focal lengths at least `1e-3` pixels. `target_from_source` is a proper float64 `(4,4)` rigid transform mapping source-camera coordinates to target-camera coordinates, translation in meters. `target_size` is int64 `(2,)` ordered `[height,width]`, each in `[1,4096]` pixels.

Camera coordinates are right-handed, x right, y down, z forward; integer pixel coordinates denote centers. Source pixels may be arbitrary finite coordinates; the caller supplies their depth hypotheses and source validity. Unproject `p=[(x-cx)/fx,(y-cy)/fy,1]/inverse_depth`, transform p, then project with target intrinsics.

Return fresh float64 `target_points (N,3)` in meters, float64 `target_pixels (N,2)`, and bool `visible (N,)`, in a dictionary. Project only when target depth is strictly greater than `1e-9` meters; otherwise target_pixels are NaN. Front-facing points outside the image retain projected coordinates, but visible is True only when `0<=x<width` and `0<=y<height`. This tests the declared image-coordinate bounds, not bilinear-stencil availability or occlusion. No distortion or image sampling is performed. Validate rotations/last rows with atol=1e-9, rtol=0; do not repair invalid transforms.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Source/target intrinsics `[2.,2.,0.,0.]`, identity transform, source pixel `[[1.,0.]]`, inverse depth `[0.5]`, target size `[4,4]` give point `[[1.,0.,2.]]`, pixel `[[1.,0.]]`, visible `[True]`.
2. Add target-from-source translation `[1.,0.,0.]` to the same example. The target point becomes `[[2.,0.,2.]]` and pixel `[[2.,0.]]`, still visible.

## Source and scope

[Primary source](https://arxiv.org/abs/1607.02565). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Unproject all source points, apply the source-to-target transform, and project only the supported positive-depth subset. Keep projected offscreen coordinates but mark them invisible. O(N) time and memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
