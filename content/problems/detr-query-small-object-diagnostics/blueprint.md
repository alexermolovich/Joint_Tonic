---
{
  "schema_version": 1,
  "problem_id": "detr-query-small-object-diagnostics",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Diagnose Query Collapse and Missed Small Objects",
  "summary": "Report highly similar query pairs and geometrically uncovered small target boxes as separate diagnostics.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "detr",
    "detr-query-small-object-diagnostics"
  ],
  "paper_ids": [
    "2020-detr"
  ],
  "paper_sections": [
    "Set prediction loss with bipartite matching; original query/coverage diagnostics"
  ],
  "track_ids": [
    "paper-2020-detr"
  ],
  "prerequisite_problem_ids": [
    "box-iou-broadcast"
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
  "entrypoint": "solution.diagnose_queries",
  "physical_contract": {
    "frames": [
      "Normalized image plane and query feature axes"
    ],
    "units": {
      "values": "image fractions and cosine similarity"
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
    "evaluator_sha256": "d496946ff88c0934ff037c8fc021cfab6456d83d297bfb3fa0c7e5066c3624cf"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2005.12872"
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

# Diagnose Query Collapse and Missed Small Objects

Implement `diagnose_queries(features: np.ndarray, predicted_boxes: np.ndarray, target_boxes: np.ndarray, cosine_limit: float, iou_limit: float, small_area: float) -> dict`.

Report highly similar query pairs and geometrically uncovered small target boxes as separate diagnostics.
features float64(Q,D),0<=Q<=256,1<=D<=128, each row norm>=1e-8. predicted_boxes float64(Q,4) and target_boxes float64(M,4),0<=M<=256, normalized xyxy in [0,1] with strictly positive width/height. Scalars are built-in non-bool int/float: cosine_limit in [-1,1], iou_limit in (0,1], small_area in [0,1]. Return {"similar_pairs":int64(K,2),"missed_small_indices":int64(L,)}. Similar pairs are i<j with normalized feature dot product>=cosine_limit, sorted lexicographically. A small target has normalized area<=small_area and is missed if every prediction has IoU<iou_limit. With Q=0 all small targets are missed. No class labels or one-to-one matching are used: coverage is class-agnostic, and similar feature pairs flag potential redundancy rather than proving query collapse.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Features `[[1,0],[2,0]]` are identical directions. Predictions both box `[0,0,0.1,0.1]`; targets that box and `[0.8,0.8,0.9,0.9]`; limits (0.99,0.5,0.02) give similar_pairs=`[[0,1]]`, missed_small_indices=`[1]`.
2. With no queries and targets `[0,0,0.1,0.1]` and `[0,0,1,1]`, small_area=0.02 returns no pairs and missing index `[0]`. Large targets are outside this slice.

## Source and scope

[Primary source](https://arxiv.org/abs/2005.12872). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Normalize query features and compare pairwise cosine; compute prediction-target IoU and small-target coverage. O(Q²D+QM) time.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
