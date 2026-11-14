# Warp a Point Between Calibrated Frames

Implement `warp_pixels(pixels, inverse_depth, source_intrinsics, target_intrinsics, target_from_source, target_size)`.

Unproject source pixels, transform their depth hypotheses, and project them into a target camera.

`pixels` is float64 `(N,2)` in `(x,y)` pixel order; `inverse_depth` is float64 `(N,)` in `[1e-6,1e6]` inverse meters; `0<=N<=16384`. Source and target intrinsics are float64 `(4,)` ordered `[fx,fy,cx,cy]`, with focal lengths at least `1e-3` pixels. `target_from_source` is a proper float64 `(4,4)` rigid transform mapping source-camera coordinates to target-camera coordinates, translation in meters. `target_size` is int64 `(2,)` ordered `[height,width]`, each in `[1,4096]` pixels.

Camera coordinates are right-handed, x right, y down, z forward; integer pixel coordinates denote centers. Source pixels may be arbitrary finite coordinates; the caller supplies their depth hypotheses and source validity. Unproject `p=[(x-cx)/fx,(y-cy)/fy,1]/inverse_depth`, transform p, then project with target intrinsics.

Return fresh float64 `target_points (N,3)` in meters, float64 `target_pixels (N,2)`, and bool `visible (N,)`, in a dictionary. Project only when target depth is strictly greater than `1e-9` meters; otherwise target_pixels are NaN. Front-facing points outside the image retain projected coordinates, but visible is True only when `0<=x<width` and `0<=y<height`. This tests the declared image-coordinate bounds, not bilinear-stencil availability or occlusion. No distortion or image sampling is performed. Validate rotations/last rows with atol=1e-9, rtol=0; do not repair invalid transforms.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Source/target intrinsics `[2.,2.,0.,0.]`, identity transform, source pixel `[[1.,0.]]`, inverse depth `[0.5]`, target size `[4,4]` give point `[[1.,0.,2.]]`, pixel `[[1.,0.]]`, visible `[True]`.
2. Add target-from-source translation `[1.,0.,0.]` to the same example. The target point becomes `[[2.,0.,2.]]` and pixel `[[2.,0.]]`, still visible.

## Source and scope

[Primary source](https://arxiv.org/abs/1607.02565). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
