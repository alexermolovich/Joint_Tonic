# Subtract a Tactile Reference Image

Subtract a comparable unloaded reference to reveal optical change. Preserve the sign of channel differences, then summarize their absolute magnitude for thresholding inside a declared region of interest.

## Contract

`images` is real `(B, H, W, C)`, `reference` is real `(H, W, C)` and `roi` is Boolean `(H, W)`. Bounds are `1 <= B <= 32`, `1 <= H, W <= 64`, `1 <= C <= 3`, and all intensities lie in `[0, 1]`. `threshold` is a scalar in `[0, 1]`. Captures and unloaded reference must share sensor, pixel alignment and exposure.

Return `difference` (float64 `(B, H, W, C)`) as signed capture-minus-reference, `change` (float64 `(B, H, W)`) as the mean absolute channel difference, and `mask` (Boolean `(B, H, W)`) where change is strictly greater than the threshold, in a dictionary. All three outputs are zero or false outside the ROI. An empty ROI returns all-zero outputs. Broadcast the reference only over the batch axis.

Image rows increase down and columns right; integer coordinates denote pixel centers. Appearance change is neither a force measurement nor proof of contact.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Example 1

For a zero one-channel reference, image [[0, 0.2], [0.1, 0.4]], an all-true ROI and threshold 0.15, the mask is [[False, True], [False, True]] and change equals the input image.

## Example 2

Image intensity 0.2 versus reference 0.8 produces signed difference -0.6 and absolute change 0.6. An excluded ROI pixel always produces zero difference/change and false mask.
