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
