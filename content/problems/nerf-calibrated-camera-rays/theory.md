# Generate Calibrated Camera Rays

## Intuition

A pixel names a direction, not a 3D position. Intrinsics undo focal scaling and principal-point offset; extrinsics orient that direction and locate its origin in the world.

## Math

For pixel $(u,v)$, focal lengths $(f_x,f_y)$ and principal point $(c_x,c_y)$, all in pixels, define
$$d_c=[(u-c_x)/f_x,(v-c_y)/f_y,1]^\top,\qquad o_w=t,\qquad d_w=\frac{Rd_c}{\|Rd_c\|_2}.$$
The camera-to-world rotation $R\in SO(3)$ maps directions; $t\in\mathbb R^3$ is the camera origin in world meters. The ray is $r(s)=o_w+s d_w$ for distance $s$ in meters because $d_w$ has unit norm. This unit-ray convention differs from implementations that retain unnormalized directions and compensate sample intervals by their norms.

| Transform | Input | Output |
|---|---|---|
| Undo intrinsics | pixel (u,v) | dimensionless camera direction |
| Rotate | camera direction | world direction |
| Normalize | world direction | unit direction |
| Translate origin | camera origin 0 | world origin t |

At $(u,v)=(1,0)$ with identity K and R, $d_c=(1,0,1)$ and norm $\sqrt2$, hence $d_w=(1/\sqrt2,0,1/\sqrt2)$. At range $s=\sqrt2$ meters from zero origin the ray reaches $(1,0,1)$ meters.

## Why this matters on a robot

Ray directions link images to depth geometry and rendering. Adding translation to a direction, using world-to-camera R without inversion, or adding a half-pixel shift twice yields plausible but systematically wrong geometry. Lens distortion must be corrected upstream.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2003.08934). [project-camera-points](/problems/project-camera-points)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
