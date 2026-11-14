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
