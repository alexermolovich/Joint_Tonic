# Compute DETR Classification, L1, and GIoU Losses

Implement `detr_losses(logits: np.ndarray, predicted_boxes: np.ndarray, target_labels: np.ndarray, target_boxes: np.ndarray, assignment: np.ndarray, eos_weight: float) -> dict`.

Compute single-image DETR losses from a supplied injective target-to-query assignment.
logits float64(Q,C+1),1<=Q<=256,1<=C<=64; final class C is no-object. predicted_boxes float64(Q,4),target_boxes float64(M,4),0<=M<=Q are normalized (cx,cy,w,h),centers[0,1],sizes[1e-6,1]. target_labels int64(M,) in[0,C),assignment int64(M,) contains unique query indices in[0,Q). eos_weight is built-in non-bool int/float in(0,1]. Assign matched queries their target class and all others no-object. classification is weighted cross entropy: sum(weight*negative log softmax chosen class)/sum(weights), with no-object weight eos_weight, all real classes weight1. l1 is sum absolute coordinate errors over matched boxes divided by max(M,1); giou is sum(1-GIoU) over matched pairs divided by max(M,1). Convert centers to corners without clipping; GIoU=IoU-(enclosing_area-union)/enclosing_area. Empty targets have l1=giou=0 and background classification. Return Python-float dict classification,l1,giou,total=classification+5*l1+2*giou. No matching solver, auxiliary decoder losses or distributed reduction.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One query,one real class,zero logits,identical predicted/target box,assignment[0]: classification=ln2,l1=giou=0,total=ln2.
2. Prediction center(0.25,0.5),size(0.5,1),target center(0.75,0.5),same size: boxes touch,so IoU=GIoU=0,l1=0.5,giou loss1. With zero two-class logits,total=ln2+2.5+2.

## Source and scope

[Primary source](https://arxiv.org/abs/2005.12872). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
