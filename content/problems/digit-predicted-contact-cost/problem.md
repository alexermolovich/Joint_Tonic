# Score Predicted Tactile Contact Outcomes

Candidate tactile predictions can be compared with a desired image before choosing a command. Separate appearance error from supplied action effort, and keep invalid candidates out of selection instead of assigning them an attractive zero score.

## Contract

`predictions` is real `(K, H, W, C)`, `goal` is real `(H, W, C)`, `roi` is Boolean `(H, W)`, `action_effort` is real `(K,)` and `valid` is Boolean `(K,)`. Bounds are `0 <= K <= 64`, `1 <= H, W <= 64` and `1 <= C <= 3`. Image intensities lie in `[0, 1]`, effort in `[0, 1000]`, and scalar `effort_weight` in `[0, 100]`. The ROI must contain at least one pixel. Prediction and goal share pixel alignment and optical/exposure conventions.

For each candidate, compute image MSE over ROI pixels and all channels. Cost equals this MSE plus `effort_weight * action_effort`. Effort is a supplied dimensionless sum of squared normalized commands; the weight gives a common dimensionless cost convention.

Return a dictionary with `image_error` and `costs` (float64 `(K,)`, NaN for invalid candidates) and `best_index` (Python int, the lowest index attaining the minimum valid cost, or -1 if no valid candidate exists). Validate all numeric entries even when their candidate or pixel is masked.

Predicted images are supplied; no dynamics model runs. This original photometric planning diagnostic does not reproduce the DIGIT controller or measure force and safety.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Example 1

Two single-pixel predictions 0 and 1, goal 0, efforts [1, 0], weight 0.2 and both candidates valid yield image errors [0, 1], costs [0.2, 1] and best index 0.

## Example 2

Two identical zero-error predictions with zero effort choose index 0. If both candidates are invalid, costs are NaN and best index is -1.
