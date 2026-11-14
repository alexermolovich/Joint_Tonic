---
{
  "schema_version": 1,
  "problem_id": "bev-visibility-mask",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Mask Out-of-View and Behind-Camera Samples",
  "summary": "Build a per-camera visibility mask from projections and signed optical depth.",
  "type": "component",
  "difficulty": "easy",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "bevformer",
    "bev-visibility-mask"
  ],
  "paper_ids": [
    "2022-bevformer"
  ],
  "paper_sections": [
    "Spatial cross-attention projection and temporal BEV alignment; gated fusion and health checks are original teaching substitutes"
  ],
  "track_ids": [
    "paper-2022-bevformer"
  ],
  "prerequisite_problem_ids": [
    "bev-project-reference-points"
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
  "entrypoint": "solution.bev_visibility",
  "physical_contract": {
    "frames": [
      "Optical camera image plane"
    ],
    "units": {
      "values": "pixels and meters"
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
    "evaluator_sha256": "01ce5a0aebee4c332b580940c33914fc39c4213ba0eef633ff92b1a8b0fe9fb6"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2203.17270"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Mask Out-of-View and Behind-Camera Samples

Implement `bev_visibility(uv: np.ndarray, depth: np.ndarray, image_sizes: np.ndarray) -> np.ndarray`.

Build a per-camera visibility mask from projections and signed optical depth.
`uv` (C,N,2) float64 stores continuous (u,v) pixels, `depth` (C,N) float64 stores meters, and `image_sizes` (C,2) int64 stores (height,width), each 1..100000. 1<=C<=16,0<=N<=4096. Return bool (C,N), true exactly when depth>1e-6, 0<=u<width, and 0<=v<height. Upper bounds are exclusive. No occlusion test or rounding is performed. Inputs are finite; invalid sentinels must retain nonpositive depth. All cameras and points refer to one synchronized instant.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. uv=`[[[0,0],[4,2],[3.9,2.9]]]`, depth=`[[1,1,1]]`, sizes=`[[3,4]]` returns `[[True,False,True]]`.
2. Three points all at pixel (1,1), depths `[-1,1e-6,2e-6]`, size (2,2), return `[False,False,True]`.

## Source and scope

[Primary source](https://arxiv.org/abs/2203.17270). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Combine three broadcast comparisons. Time and returned storage O(CN).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
