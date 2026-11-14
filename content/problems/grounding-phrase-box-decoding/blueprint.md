---
{
  "schema_version": 1,
  "problem_id": "grounding-phrase-box-decoding",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Decode Phrase-Labeled Boxes",
  "summary": "Associate each normalized box with its strongest phrase, then return thresholded pixel boxes.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "grounding-dino",
    "grounding-phrase-box-decoding"
  ],
  "paper_ids": [
    "2023-grounding-dino"
  ],
  "paper_sections": [
    "Language-guided query selection and text-grounded box outputs; phrase aggregation and orchestration are declared teaching contracts"
  ],
  "track_ids": [
    "paper-2023-grounding-dino"
  ],
  "prerequisite_problem_ids": [
    "grounding-token-phrase-map"
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
  "entrypoint": "solution.decode_grounded_boxes",
  "physical_contract": {
    "frames": [
      "Normalized image plane to original pixel image"
    ],
    "units": {
      "values": "image fractions, pixels and probabilities"
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
    "evaluator_sha256": "86a188b6f72783fc0ed92fbdb51845f479c91e7842a9cf4aa4b4eff01f90a98e"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.05499"
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

# Decode Phrase-Labeled Boxes

Implement `decode_grounded_boxes(boxes: np.ndarray, token_logits: np.ndarray, phrase_map: np.ndarray, image_size: tuple[int,int], threshold: float) -> dict`.

Associate each normalized box with its strongest phrase, then return thresholded pixel boxes.
boxes float64 (Q,4) contains normalized image (cx,cy,width,height), all values in [0,1], positive width/height;0<=Q<=2048. token_logits float64 (Q,T),1<=T<=512. phrase_map bool (P,T),1<=P<=128; every phrase must have at least one token. image_size is tuple (height,width) built-in positive ints<=100000. threshold is built-in non-bool int/float in [0,1]. Sigmoid each token logit stably. A phrase score is MAX probability over its mapped tokens (a declared teaching aggregation); choose highest phrase per query, ties lower phrase index. Keep score>=threshold in original query order. Return exactly query_indices int64(K,), phrase_indices int64(K,), scores float64(K,), boxes_xyxy float64(K,4). Convert normalized center-size to pixel corners without clipping; boxes can extend outside the image. No NMS or tokenizer runs.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Box `[0.5,0.5,0.5,1]`, two zero logits, phrase_map=I₂ bool, image (100,200), threshold=0.5 yields query0, phrase0 (tie), score0.5, corners `[50,0,150,100]`.
2. Box `[0,0,1,1]`, one logit0, one phrase, image (10,20), threshold=0.5 yields `[-10,-5,10,5]`. Coordinates remain unclipped.

## Source and scope

[Primary source](https://arxiv.org/abs/2303.05499). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Use stable sigmoid, phrase-wise maxima, deterministic argmax, then convert selected boxes. Time O(QPT), storage O(QP).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
