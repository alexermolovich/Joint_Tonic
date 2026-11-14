# Project BEV Reference Points into Calibrated Cameras

## Intuition

One BEV reference point can be seen by several cameras. Its pixel position depends on both the camera pose and calibration; retaining depth separately makes front/behind decisions explicit.

## Math and pipeline

For ego point $p_e\in\mathbb R^3$ in meters and camera index $c$, $R_c$ and $t_c$ map ego coordinates to optical coordinates:
$$p_c=R_c p_e+t_c,\qquad z_c=(p_c)_z,\qquad (u_c,v_c)=\left(f_{x,c}\frac{(p_c)_x}{z_c}+c_{x,c},f_{y,c}\frac{(p_c)_y}{z_c}+c_{y,c}\right).$$
Focal lengths and principal points are pixels. Division is performed only for $z_c>10^{-6}$ meters; other pixels use a zero sentinel. That cutoff is a numerical contract, not a collision margin.

| Data | Shape | Interpretation |
|---|---|---|
| Ego references | N × 3 | Same points for every camera |
| Optical points | C × N × 3 | Per-camera transformed points |
| Depth | C × N | Signed optical z |
| Projection | C × N × 2 | Pixel coordinates before visibility filtering |

For $p_e=(2,4,2)$ and identity transforms/intrinsics, division by depth 2 gives $(u,v)=(1,2)$. A point at negative depth has no usable forward projection even when dividing it would give an in-bounds number.

## Why this matters on a robot

Wrong transform direction can silently place features in the wrong BEV cell. A visible pixel at the image origin must not be confused with the invalid sentinel; consumers must also check depth. This component does not generate BEV grids or implement deformable attention.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2203.17270). [se3-transform-points](/problems/se3-transform-points) · [project-camera-points](/problems/project-camera-points)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
