---
{
  "schema_version": 1,
  "problem_id": "grounded-segmentation-failure-trace",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Build a Grounded Segmentation Pipeline and Trace Failures",
  "summary": "Compose supplied grounding and segmentation outputs while preserving failure reasons per query.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "grounding-dino",
    "grounded-segmentation-failure-trace"
  ],
  "paper_ids": [
    "2023-grounding-dino",
    "2023-segment-anything"
  ],
  "paper_sections": [
    "Language-guided query selection and text-grounded box outputs; phrase aggregation and orchestration are declared teaching contracts"
  ],
  "track_ids": [
    "paper-2023-grounding-dino"
  ],
  "prerequisite_problem_ids": [
    "grounding-phrase-box-decoding",
    "sam-mask-ranking"
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
  "entrypoint": "solution.grounded_segmentation",
  "physical_contract": {
    "frames": [
      "Original image pixels; query/mask identity aligned"
    ],
    "units": {
      "values": "probabilities and pixel areas/centers"
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
    "evaluator_sha256": "edcdf99ef1bb73c2f3af45341852bde4ea28404a9f5e9d4c419f10fe42d0a37b"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.05499",
      "https://arxiv.org/abs/2304.02643"
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

# Build a Grounded Segmentation Pipeline and Trace Failures

Implement `grounded_segmentation(phrase_scores: np.ndarray, masks: np.ndarray, mask_quality: np.ndarray, min_phrase: float, min_quality: float) -> dict`.

Compose supplied grounding and segmentation outputs while preserving failure reasons per query.
phrase_scores float64 (Q,P) in [0,1],0<=Q<=128,1<=P<=128. masks bool(Q,H,W),1<=H,W<=128 are already decoded in one original image frame and correspond one-to-one to query rows. mask_quality float64(Q,) in [0,1] is predicted mask quality, not true IoU. Thresholds are built-in non-bool int/float in [0,1]. Choose highest phrase score per query, ties smaller phrase index. Give each query exactly one status string, in precedence: "low_grounding" if best phrase score<min_phrase; otherwise "low_mask_quality" if quality<min_quality; otherwise "empty_mask" if no foreground pixels; otherwise "accepted". Return {"status":list[str] length Q,"query_indices":int64(K,),"phrase_indices":int64(K,),"areas":int64(K,),"centroids_xy":float64(K,2)} for accepted queries in original order. Area counts foreground pixels; centroid is mean of pixel-center coordinates (column+0.5,row+0.5). This pipeline consumes synthetic model outputs; it does not load models or execute a grasp.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One query scores `[0.9,0.2]`, quality0.8, mask `[[True,True],[False,False]]`, thresholds(0.5,0.5): accepted, phrase0, area2, centroid `[1,0.5]` pixels.
2. Two empty masks, best scores `[0.2,0.9]`, qualities `[0.1,0.1]`, thresholds(0.5,0.5) report `["low_grounding","low_mask_quality"]`. Earlier failures take precedence over emptiness.

## Source and scope

[Primary source](https://arxiv.org/abs/2303.05499). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Check stages in order, then reduce accepted mask coordinates. O(Q(P+HW)) time.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
