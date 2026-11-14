---
{
  "schema_version": 1,
  "problem_id": "sample-keypoint-descriptors",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Sample Descriptors at Keypoint Coordinates",
  "summary": "Interpolate descriptor vectors at image keypoints with an explicit image-to-grid mapping.",
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
  "prerequisite_problem_ids": [
    "homographic-keypoint-adaptation"
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
  "entrypoint": "solution.sample_descriptors",
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
    "evaluator_sha256": "f398e9f204caf355d96f1da9853a9c08c9d4c58b8dc2521ca14fe5df083e1f34"
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

# Sample Descriptors at Keypoint Coordinates

Implement `sample_descriptors(descriptor_map, keypoints, stride, offset)`.

Interpolate descriptor vectors at image keypoints with an explicit image-to-grid mapping.

`descriptor_map` is float64 `(H,W,D)`, `1<=H,W,D<=128`, `H*W*D<=1_000_000`, values with absolute magnitude <=100. `keypoints` is float64 `(N,2)` in `(x,y)` pixels, `0<=N<=4096`, `N*D<=524288`. `stride` is float64 `(2,)`, x/y pixels per grid cell in `[1e-3,64]`; `offset` is float64 `(2,)`, the image pixel coordinate of descriptor grid center `(0,0)`.

Grid coordinates are `(keypoint-offset)/stride`. A sample is geometrically valid only inside the closed center domain `[0,W-1] x [0,H-1]`. Bilinearly interpolate four neighbors, clamping an upper neighbor to the final index at a boundary. Singleton dimensions are allowed. If the sampled vector has L2 norm strictly greater than 1e-12, divide by that norm; otherwise return a zero vector.

Return `descriptors`, fresh float64 `(N,D)`, and `valid`, bool `(N,)`, in a dictionary. Invalid locations return zeros. The validity flag concerns geometry, so a valid zero descriptor remains flagged True. This is an explicit bilinear teaching variant: the paper reports bicubic descriptor sampling. No detector, suppression or learned decoder is implemented.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Descriptor map `[[[1.,0.],[0.,1.]]]`, keypoint `[[0.5,0.]]`, stride `[1.,1.]`, offset `[0.,0.]`: the sampled vector `[0.5,0.5]` becomes `[1/sqrt(2),1/sqrt(2)]`, valid True.
2. Keypoint `[[-1.,0.]]` with that map and mapping is outside the descriptor grid, so the result is `[0.,0.]`, valid False. A valid zero-valued map also returns zero, but valid True.

## Source and scope

[Primary source](https://arxiv.org/abs/1712.07629). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Convert keypoints to descriptor coordinates, sample four channel vectors, and normalize only nonzero interpolants. O(ND) time and output memory. Keep geometric support separate from descriptor magnitude.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
