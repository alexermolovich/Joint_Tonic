---
{
  "schema_version": 1,
  "problem_id": "feature-matching-score-matrix",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Build a Feature-Matching Score Matrix",
  "summary": "Compute pairwise scores from two supplied sets of learned image descriptors.",
  "type": "component",
  "difficulty": "easy",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "superglue"
  ],
  "paper_ids": [
    "2019-superglue"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2019-superglue"
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
  "entrypoint": "solution.feature_scores",
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
    "evaluator_sha256": "47837073b976287ff77dca62fe3b493b6586e0dd827631e012bae684f1b0ab27"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1911.11763"
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

# Build a Feature-Matching Score Matrix

Implement `feature_scores(source_descriptors, target_descriptors)`.

Compute pairwise scores from two supplied sets of learned image descriptors.

`source_descriptors` is float64 `(N,D)` and `target_descriptors` float64 `(M,D)`, `0<=N,M<=1024`, `N*M<=262144`, `1<=D<=128`, all values with absolute magnitude <=100. Descriptor channels are dimensionless. Return a fresh float64 `(N,M)` matrix with `S[i,j]=dot(source_descriptors[i],target_descriptors[j])/sqrt(D)`.

Descriptors need not have unit norm. Do not normalize descriptor rows, apply softmax, or add dustbins. Empty point sets return the exact corresponding empty matrix shape. This isolates an explicit supplied-feature similarity convention; the descriptors are already produced by a separate learned network. It does not implement contextual graph refinement or training.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With D=1, source `[[2.],[3.]]` and target `[[4.]]` give scores `[[8.],[12.]]`.
2. With D=4 and both sets containing one descriptor `[1.,1.,1.,1.]`, the dot product 4 is divided by sqrt(4), giving `[[2.]]`. Cosine similarity would incorrectly give 1.

## Source and scope

[Primary source](https://arxiv.org/abs/1911.11763). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Multiply the source matrix by the target transpose and divide by the square root of the common channel count. O(NMD) arithmetic and O(NM) output storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
