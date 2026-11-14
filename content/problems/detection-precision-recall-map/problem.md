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
