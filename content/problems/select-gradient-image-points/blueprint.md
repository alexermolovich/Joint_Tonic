---
{
  "schema_version": 1,
  "problem_id": "select-gradient-image-points",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Select High-Gradient Image Points",
  "summary": "Select spatially distributed image points with strong central-difference intensity gradients.",
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
  "prerequisite_problem_ids": [],
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
  "entrypoint": "solution.select_gradient_points",
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
    "evaluator_sha256": "7416b48dd0e6c5d331f0c3626a6c163479604f89ae36ba9f64826a4f17ac2377"
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

# Select High-Gradient Image Points

Implement `select_gradient_points(image, tile_size, threshold)`.

Select spatially distributed image points with strong central-difference intensity gradients.

`image` is float64 `(H,W)`, `3<=H,W<=1024`, `H*W<=1_000_000`, intensities in `[0,1]`. `tile_size` is a Python int in `[1,128]`; `threshold` a Python int/float in `[0,1]`. Pixel centers use integer `(x=column,y=row)` coordinates, x right and y down. Gradients are intensity per pixel.

For each interior pixel compute `dx=(image[y,x+1]-image[y,x-1])/2`, `dy=(image[y+1,x]-image[y-1,x])/2`, score `sqrt(dx**2+dy**2)`. Exclude the outermost pixel border. Partition the full image into tiles starting at `(0,0)`, with height/width tile_size; partial edge tiles remain. Within each tile choose at most one interior pixel, the highest score strictly greater than threshold. Exact ties choose the smallest row-major image index.

Return a dictionary with fresh int64 `coordinates (K,2)` in `(x,y)` order and float64 `scores (K,)`; emit selected points in tile row-major order. Empty selections are valid. This original fixed-tile selector illustrates spatial gradient coverage; it is not DSO's exact adaptive, multiscale pixel-selection algorithm.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. A `5x5` image whose rows are `[0.,0.25,0.5,0.75,1.]`, tile size `5`, threshold `0.1` yields coordinates `[[1,1]]` and score `[0.25]`. Every interior pixel ties; choose the earliest row-major one.
2. A constant `3x3` image, tile size `1`, threshold `0` returns empty coordinates of shape `(0,2)` and empty scores. Zero gradient does not exceed the threshold.

## Source and scope

[Primary source](https://arxiv.org/abs/1607.02565). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute gradients only on the interior. Associate eligible pixels with tile IDs, then lexicographically sort by tile, descending score and original pixel index; retain the first pixel of each tile. O(HW log(HW)) worst-case time and O(HW) memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
