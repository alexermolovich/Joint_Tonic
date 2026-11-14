# Compute Point-to-Line and Point-to-Plane Scan Residuals

Implement `scan_residuals(plane_points, plane_anchors, plane_normals, line_points, line_a, line_b, world_from_lidar)`.

Compute signed point-to-plane and unsigned point-to-line residuals after transforming scan features into the map frame.

`plane_points`, `plane_anchors`, `plane_normals` are float64 `(P,3)`; `line_points`, `line_a`, `line_b` are float64 `(L,3)`; `0<=P,L<=8192`. Scan points are in one synchronized lidar frame; plane anchors/normals and line endpoints are in a common world/map frame. Points and translations use meters. `world_from_lidar` is a proper float64 `(4,4)` rigid transform, validated with atol=1e-9, rtol=0 for its rotation and last row.

Every plane normal must have norm within `1e-9` of one; normalize accepted normals. Every line's endpoints must be separated by at least `1e-6` meters. Transform each scan point to the world frame. Return a dictionary with fresh float64 `plane (P,) = normal dot (world_point-plane_anchor)` and `line (L,) = norm(cross(world_point-line_a,line_b-line_a))/norm(line_b-line_a)`, both in meters. Plane sign follows the supplied normal; line distances are nonnegative. Empty groups are allowed. No nearest-neighbor association, robust loss, filtering or pose update is performed. This one package supplies both the FAST-LIO2 point-to-plane kernel and LIO-SAM-style line/plane feature residual practice.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With identity transform, plane scan point `[[0.,0.,2.]]`, anchor `[[0.,0.,0.]]` and normal `[[0.,0.,1.]]`, the signed plane residual is `[2.]` meters. Line scan point `[[0.,1.,0.]]`, endpoints `[[0.,0.,0.]]` and `[[2.,0.,0.]]` give line distance `[1.]` meter.
2. Keep the plane point and anchor but negate the normal: plane residual is `[-2.]`. Reversing a line's endpoint order leaves its nonnegative distance unchanged.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.00258). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
