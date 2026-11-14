# Deskew a Lidar Scan with Motion Estimates

Implement `deskew_points(points, world_from_capture, world_from_reference)`.

Express points captured at different instants in one reference lidar frame using supplied per-point poses.

`points` is float64 `(N,3)` meters, `0<=N<=8192`. `world_from_capture` is float64 `(N,4,4)`, where transform i maps the lidar frame at point i's capture time into a common world frame. `world_from_reference` is float64 `(4,4)`, mapping the desired reference lidar frame into the same world. All transforms must be proper rigid transforms with rotation/last-row checks atol=1e-9, rtol=0.

Return a fresh float64 `(N,3)` array in reference-lidar coordinates, using `inverse(world_from_reference) @ world_from_capture[i] @ homogeneous(points[i])`. The reference frame may be any caller-selected scan time; the poses already include the intended lidar extrinsic convention. Empty scans are valid. Pose estimates are supplied exactly aligned per point; do not infer timestamps, interpolate poses, integrate IMU data or estimate extrinsics. This geometric deskew component is distinct from applying one static transform to a synchronized cloud.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One captured point `[[2.,0.,0.]]`, capture pose with identity rotation and world translation `[1.,0.,0.]`, and identity reference pose yield `[[3.,0.,0.]]` in the reference lidar frame.
2. Change the reference pose's world translation to `[2.,0.,0.]`. The same capture and point now yield `[[1.,0.,0.]]` in the reference lidar frame.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.00258). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
