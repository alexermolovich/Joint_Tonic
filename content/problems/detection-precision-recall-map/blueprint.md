---
{
  "schema_version": 1,
  "problem_id": "detection-precision-recall-map",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Evaluate Detection with IoU, Precision-Recall, and mAP",
  "summary": "Evaluate class-aware image-local detection precision/recall and interpolated AP at ONE IoU threshold.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "yolo-v1",
    "detection-precision-recall-map"
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
    "box-iou-broadcast",
    "class-aware-nms"
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
  "entrypoint": "solution.detection_map",
  "physical_contract": {
    "frames": [
      "Normalized image plane plus explicit image/class identities"
    ],
    "units": {
      "values": "image fractions and dimensionless metrics"
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
    "evaluator_sha256": "5ae328f94ea9660d8ca18500cd7fc73ea7fa15534c36469c7dc23364d84f0b19"
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

# Evaluate Detection with IoU, Precision-Recall, and mAP

Implement `detection_map(pred_boxes: np.ndarray, scores: np.ndarray, pred_labels: np.ndarray, pred_images: np.ndarray, target_boxes: np.ndarray, target_labels: np.ndarray, target_images: np.ndarray, num_classes: int, iou_threshold: float) -> dict`.

Evaluate class-aware image-local detection precision/recall and interpolated AP at ONE IoU threshold.
pred_boxes float64(N,4),target_boxes float64(M,4) are normalized xyxy in[0,1] with positive width/height;0<=N,M<=512. scores float64(N,) in[0,1]. Labels are int64 vectors length N/M in[0,num_classes); image IDs int64 vectors length N/M in[0,1000000]. num_classes built-in int1..64, iou_threshold built-in non-bool int/float in(0,1]. For each class sort predictions by descending score then original prediction index. Find highest-IoU target of same class AND image; ties choose smallest original target index. TP iff that IoU>=threshold and that best target has not already been matched. Otherwise FP; do not fall back to a second-best unmatched target. Precision is cumulativeTP/rank; recall=cumulativeTP/number_of_class_targets (zero if none). AP uses the nonincreasing precision envelope integrated over all recall increases, not VOC2007 11-point or COCO multi-threshold AP. Return dict ap float64(C,) (NaN for classes with no targets), mean_ap Python float (mean over classes with targets,0 if none), and precision/recall lists of C float64 vectors in class-local score order. No ignored/crowd boxes or NMS.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One class/two targets in one image. Predictions score0.9 correct targetA,score0.8 duplicateA,score0.7 correctB give precision `[1,0.5,2/3]`,recall `[0.5,0.5,1]`, AP=5/6 via the precision envelope.
2. A class with one target and no predictions has AP0. A second class with no targets has AP NaN and is excluded from mean_ap, so mean_ap=0.

## Source and scope

[Primary source](https://arxiv.org/abs/1506.02640). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Sort predictions per class, perform image-local overlap matching and integrate precision envelopes. O(NM+N log N+C) time, bounded synthetic arrays.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
