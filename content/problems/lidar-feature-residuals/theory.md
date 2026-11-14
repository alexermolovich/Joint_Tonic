# Compute Point-to-Line and Point-to-Plane Scan Residuals

## Intuition

A plane constrains motion along its normal, while a line measures perpendicular separation. Apply the lidar-to-map transform before evaluating either relation; a correct formula in the wrong frame is still wrong.

## Mathematics and conventions

For lidar point $p$, rigid transform $(R,t)$ and plane anchor q with unit normal n,

$$p_w=Rp+t,\qquad r_{plane}=n^T(p_w-q).$$

For line endpoints a,b with nonzero separation,

$$r_{line}=\frac{\|(p_w-a)\times(b-a)\|_2}{\|b-a\|_2}.$$

All points are meters in their declared frames, R and n are dimensionless, and both residuals are meters. The cross-product numerator has square-meter units. Reversing n flips a plane residual; reversing the line direction does not change line distance.

## Visual computation trace

| Feature | World scan point | Geometry | Residual |
| --- | --- | --- | --- |
| Plane | (0,0,2) | z=0, normal +z | +2 m |
| Same plane | (0,0,2) | normal -z | -2 m |
| Line | (0,1,0) | x axis | 1 m |

## Worked examples

1. With identity transform, plane scan point `[[0.,0.,2.]]`, anchor `[[0.,0.,0.]]` and normal `[[0.,0.,1.]]`, the signed plane residual is `[2.]` meters. Line scan point `[[0.,1.,0.]]`, endpoints `[[0.,0.,0.]]` and `[[2.,0.,0.]]` give line distance `[1.]` meter.
2. Keep the plane point and anchor but negate the normal: plane residual is `[-2.]`. Reversing a line's endpoint order leaves its nonnegative distance unchanged.

## Why this matters on a robot

A scene with only one plane leaves some motion directions unobservable. Small residuals alone do not imply the pose is well constrained; association quality and inertial information remain separate concerns.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2007.00258). [se3-transform-points](/problems/se3-transform-points)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
