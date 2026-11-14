# Apply Homographic Keypoint Adaptation

Implement `adapt_keypoints(probabilities, homographies, output_size)`.

Aggregate detector probability maps into a reference image using known projective warps.

`probabilities` is float64 `(K,H,W)`, with `1<=K<=16`, `1<=H,W<=256`, `K*H*W<=1_000_000`, values in `[0,1]`. `homographies` is float64 `(K,3,3)` mapping reference-image homogeneous coordinates to each warped detector map. Each matrix has absolute entries <=1000 and absolute determinant >=1e-9; do not rescale it. `output_size` is int64 `(2,)` `[height,width]`, each 1..256.

Coordinates `(x,y)` use integer pixel centers, x right/y down. For every reference pixel, apply each homography, divide by the third homogeneous coordinate only when its absolute value is strictly greater than 1e-9. Bilinearly sample that detector map only inside the closed center rectangle `0<=x<=W-1, 0<=y<=H-1`. At the last center, clamp the upper interpolation neighbor to the last index; singleton dimensions are valid. Average supported samples only.

Return a dictionary with fresh float64 `probability (output_height,output_width)` (NaN with no support) and int64 `count` of the same shape. This is the aggregation component, using an explicit boundary/interpolation policy. Detector inference, random homography generation, border erosion and multiscale training are outside this exercise.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Two identity-warped `2x2` constant maps, with values 0.2 and 0.8, produce a `2x2` map of 0.5 and counts 2.
2. One map `[[0.2,0.8]]`, reference-to-warped x translation +1, output size `[1,2]`, gives probability `[[0.8,NaN]]` and count `[[1,0]]`. The missing sample is not a zero detection.

## Source and scope

[Primary source](https://arxiv.org/abs/1712.07629). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
