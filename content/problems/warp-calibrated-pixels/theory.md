# Warp a Point Between Calibrated Frames

## Intuition

A pixel and inverse depth define a ray point in the source camera. The transform direction matters: move that 3D point into the target frame before dividing by its new depth.

## Mathematics and conventions

Let pixel $u=(x,y)$, inverse depth $\rho$ in inverse meters, intrinsics $(f_x,f_y,c_x,c_y)$ in pixels, and transform $(R,t)$ from source to target.

$$p_s=\rho^{-1}\begin{bmatrix}(x-c_x)/f_x\\(y-c_y)/f_y\\1\end{bmatrix},\qquad p_t=Rp_s+t.$$

For positive supported target depth $Z>10^{-9}$ meters, use target intrinsics to compute

$$x'=f'_x X/Z+c'_x,\qquad y'=f'_y Y/Z+c'_y.$$

Finite image bounds are checked after projection. A front-facing offscreen projection remains a valid geometric result even though its visibility flag is false. Behind-camera projection is deliberately undefined and represented by NaN.

## Visual computation trace

| Stage | Identity cameras | Target shifted +1 m in x |
| --- | --- | --- |
| Pixel/rho | (1,0), 0.5 inverse m | same |
| Source point | (1,0,2) m | same |
| Target point | (1,0,2) m | (2,0,2) m |
| Target pixel | (1,0) | (2,0) |

## Worked examples

1. Source/target intrinsics `[2.,2.,0.,0.]`, identity transform, source pixel `[[1.,0.]]`, inverse depth `[0.5]`, target size `[4,4]` give point `[[1.,0.,2.]]`, pixel `[[1.,0.]]`, visible `[True]`.
2. Add target-from-source translation `[1.,0.,0.]` to the same example. The target point becomes `[[2.,0.,2.]]` and pixel `[[2.,0.]]`, still visible.

## Why this matters on a robot

Using the inverse transform produces the wrong optical flow sign. Visibility here excludes negative depth and coordinate overflow but does not detect occlusion or validate an interpolation neighborhood.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1607.02565). [project-camera-points](/problems/project-camera-points) · [se3-transform-points](/problems/se3-transform-points)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
