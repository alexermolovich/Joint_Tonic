---
{
  "schema_version": 1,
  "problem_id": "local-window-match-expectation",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Refine a Match in a Local Window",
  "summary": "Refine target keypoint positions using a probability distribution over a supplied local descriptor window.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "loftr"
  ],
  "paper_ids": [
    "2021-loftr"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2021-loftr"
  ],
  "prerequisite_problem_ids": [
    "dual-softmax-coarse-matches"
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
  "entrypoint": "solution.refine_matches",
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
    "evaluator_sha256": "86f4cbfdf63162ce446004c870c55f1f5bab140e864b7437c402fdd1be390fd6"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2104.00680"
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

# Refine a Match in a Local Window

Implement `refine_matches(queries, windows, coarse_targets, pixel_scale)`.

Refine target keypoint positions using a probability distribution over a supplied local descriptor window.

`queries` is float64 `(B,D)`, `windows` float64 `(B,S,S,D)`, `0<=B<=256`, `1<=D<=64`, S odd in 1..9, total window entries <=1_000_000. Query/window entries have absolute magnitude <=100. `coarse_targets` is float64 `(B,2)` target-image `(x,y)` pixels. `pixel_scale` is float64 `(2,)`, x/y pixels per window-grid cell in `[1e-3,64]`.

For each batch row compute the query/window dot products divided by sqrt(D), then a stable softmax across all S squared cells. Cell offsets are `(column-S//2,row-S//2)`, scaled elementwise into pixel offsets. Compute their probability-weighted mean and population covariance, including off-diagonal covariance.

Return fresh float64 arrays: `probabilities (B,S,S)`, `offsets (B,2)` in pixels, `refined (B,2)=coarse_targets+offsets` in pixels, and `covariance (B,2,2)` in square pixels. With S=1 the offset/covariance are zero; empty B returns exact empty shapes. Features are supplied after any fine transformer. This local-expectation component includes an explicit pixel covariance diagnostic; it is not the paper's full fine network or its normalized uncertainty head.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Zero query/window descriptors with S=3 yield uniform probability 1/9. With pixel_scale `[1.,1.]`, the offset is `[0.,0.]` and covariance `[[2/3,0],[0,2/3]]`. Scale `[2.,3.]` changes it to `[[8/3,0],[0,6]]`.
2. D=1, query 1, a `3x3` window with center value log(8) and all others zero gives center probability 1/2 and every other cell 1/16. Its offset is zero and covariance is `[[0.375,0],[0,0.375]]` at unit scale.

## Source and scope

[Primary source](https://arxiv.org/abs/2104.00680). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute each local softmax, then its first and second centered moments in pixel coordinates. O(B*S^2*D) time and O(B*S^2+B*S^2*2) temporary memory. No global image correspondence matrix is needed.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
