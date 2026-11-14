---
{
  "schema_version": 1,
  "problem_id": "yolo-coordinate-objectness-class-loss",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Compute YOLO Coordinate, Objectness, and Class Losses",
  "summary": "Compute the squared-error components of a bounded YOLO-v1 training objective from supplied responsibilities.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "yolo-v1",
    "yolo-coordinate-objectness-class-loss"
  ],
  "paper_ids": [
    "2016-yolo-v1"
  ],
  "paper_sections": [
    "Unified detection grid and training objective; downstream evaluation teaching protocol explicitly distinguished"
  ],
  "track_ids": [
    "paper-2016-yolo-v1"
  ],
  "prerequisite_problem_ids": [
    "yolo-responsible-cell-targets"
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
  "entrypoint": "solution.yolo_loss",
  "physical_contract": {
    "frames": [
      "YOLO image grid; local centers and image-relative sizes"
    ],
    "units": {
      "values": "dimensionless boxes/probabilities/losses"
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
    "evaluator_sha256": "91d45337e3dfb5b0beacfb6df6f1c300faedde49f8e92eb3f49893b99ba6312b"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1506.02640"
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

# Compute YOLO Coordinate, Objectness, and Class Losses

Implement `yolo_loss(predicted_boxes: np.ndarray, confidence: np.ndarray, class_probabilities: np.ndarray, target_boxes: np.ndarray, target_labels: np.ndarray, responsible: np.ndarray, target_iou: np.ndarray) -> dict`.

Compute the squared-error components of a bounded YOLO-v1 training objective from supplied responsibilities.
predicted_boxes float64(S,S,B,4) and target_boxes float64(S,S,4) store cell-local center x,y in [0,1], image-relative width,height in [1e-6,1]. 1<=S<=16,1<=B<=8. confidence float64(S,S,B) in [0,1], class_probabilities float64(S,S,C),1<=C<=64, entries[0,1] and row sums1 within absolute tolerance1e-8. target_labels int64(S,S) is -1 for empty cells, otherwise0..C-1. responsible int64(S,S) must be -1 exactly for empty cells, otherwise0..B-1. target_iou float64(S,S) in[0,1] is supplied confidence target for responsible boxes; validate all ignored targets too. Return Python-float dict coordinate,objectness,classification,total. Coordinate sum over occupied cells:5*((x-x*)²+(y-y*)²+(√w-√w*)²+(√h-√h*)²). Objectness: squared confidence error against supplied IoU for responsible predictors, plus0.5*confidence² for EVERY nonresponsible predictor (including occupied cells). Classification: squared distance from the cell's one-hot class, occupied cells only. Total sums components without averaging. No assignment/IoU computation or gradient is returned.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One occupied cell/predictor/class with identical boxes, confidence1,target_iou1,class_probability1 gives all losses0.
2. S=1,B=2,C=2, responsible0,target class0. Responsible width0.25 versus target width1 (all other coordinates equal) gives coordinate1.25. Confidences[0.5,0.2],target_iou1 give objectness0.25+0.02=0.27. Class probabilities[0.8,0.2] give0.08. Total1.60.

## Source and scope

[Primary source](https://arxiv.org/abs/1506.02640). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Gather occupied responsible boxes and class rows, compute masked component sums. O(S²(B+C)) time.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
