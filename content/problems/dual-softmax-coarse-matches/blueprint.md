---
{
  "schema_version": 1,
  "problem_id": "dual-softmax-coarse-matches",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Construct Coarse Correspondence Candidates",
  "summary": "Construct coarse correspondences with masked dual-softmax confidence and reciprocal choices.",
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
    "feature-matching-score-matrix",
    "extract-mutual-feature-matches"
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
  "entrypoint": "solution.coarse_matches",
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
    "evaluator_sha256": "5dedf3c50e780e485b8e095bdb479b3f97c1eb1bd1bff078c224010f1b7e8d01"
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

# Construct Coarse Correspondence Candidates

Implement `coarse_matches(source, target, source_valid, target_valid, temperature, threshold)`.

Construct coarse correspondences with masked dual-softmax confidence and reciprocal choices.

`source (N,D)` and `target (M,D)` are float64, `0<=N,M<=512`, `1<=D<=128`, absolute entries <=100. `source_valid (N,)` and `target_valid (M,)` are bool. `temperature` is a Python int/float in `[1e-3,100]`; `threshold` in `[0,1]`.

Compute dimensionless similarities `S=source@target.T/(D*temperature)`. The factor D corresponds to dividing each descriptor by sqrt(D) before forming its dot product. A pair is valid iff both endpoints are valid. Compute row softmax over valid target columns and column softmax over valid source rows, multiply the two probabilities, and set invalid pairs to zero. If an axis has no valid support, its confidence values are zero.

Choose each valid source's first maximal real target confidence and each valid target's first maximal real source confidence. Retain reciprocal pairs with confidence strictly greater than threshold. Return fresh float64 `confidence (N,M)`, int64 `pairs (K,2)` in ascending source order, and float64 `match_confidence (K,)`. Empty or fully masked sides return zero confidence and no pairs. First-index ties are a deterministic teaching convention. Border-removal heuristics, training padding, positional encoding and full network inference are outside this component.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Two zero source descriptors and two zero target descriptors, D=1, all valid, temperature 1: every confidence is 0.25. At threshold 0, first-index mutual ties retain only `[[0,0]]`; at threshold 0.25 no match survives.
2. Mask the second target in that example: the first column confidence is `[0.5,0.5]` and the second column zero. Only `[[0,0]]` survives at threshold 0.

## Source and scope

[Primary source](https://arxiv.org/abs/2104.00680). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Gather valid descriptor rows before normalizing similarities independently along the two axes. Multiply probabilities and select reciprocal confident maxima, then map indices back to the original point sets. O(NMD+NM) time and O(NM) memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
