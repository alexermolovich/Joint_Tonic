---
{
  "schema_version": 1,
  "problem_id": "homographic-keypoint-adaptation",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Apply Homographic Keypoint Adaptation",
  "summary": "Aggregate detector probability maps into a reference image using known projective warps.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "superpoint"
  ],
  "paper_ids": [
    "2017-superpoint"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2017-superpoint"
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
  "entrypoint": "solution.adapt_keypoints",
  "physical_contract": {
    "frames": [
      "Image pixel coordinates x right, y down; feature channels dimensionless"
    ],
    "units": {
      "values": "Pixels for geometry, dimensionless confidence and descriptors"
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
    "evaluator_sha256": "a0db04b77206bfdc336e11c2cd21546e8ff8dfc093341144afa3f3725d18c1df"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1712.07629"
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

# Apply Homographic Keypoint Adaptation

Implement `adapt_keypoints(probabilities, homographies, output_size)`.

Aggregate detector probability maps into a reference image using known projective warps.

`probabilities` is float64 `(K,H,W)`, with `1<=K<=16`, `1<=H,W<=256`, `K*H*W<=1_000_000`, values in `[0,1]`. `homographies` is float64 `(K,3,3)` mapping reference-image homogeneous coordinates to each warped detector map. Each matrix has absolute entries <=1000 and absolute determinant >=1e-9; do not rescale it. `output_size` is int64 `(2,)` `[height,width]`, each 1..256.

Coordinates `(x,y)` use integer pixel centers, x right/y down. For every reference pixel, apply each homography, divide by the third homogeneous coordinate only when its absolute value is strictly greater than 1e-9. Bilinearly sample that detector map only inside the closed center rectangle `0<=x<=W-1, 0<=y<=H-1`. At the last center, clamp the upper interpolation neighbor to the last index; singleton dimensions are valid. Average supported samples only.

Return a dictionary with fresh float64 `probability (output_height,output_width)` (NaN with no support) and int64 `count` of the same shape. This is the aggregation component, using an explicit boundary/interpolation policy. Detector inference, random homography generation, border erosion and multiscale training are outside this exercise.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Two identity-warped `2x2` constant maps, with values 0.2 and 0.8, produce a `2x2` map of 0.5 and counts 2.
2. One map `[[0.2,0.8]]`, reference-to-warped x translation +1, output size `[1,2]`, gives probability `[[0.8,NaN]]` and count `[[1,0]]`. The missing sample is not a zero detection.

## Source and scope

[Primary source](https://arxiv.org/abs/1712.07629). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Build the output center grid once. For each supplied warp, project and bilinearly sample supported points, accumulating sums and counts. O(K*output_height*output_width) time and O(output_height*output_width) working memory beyond the returned arrays.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
