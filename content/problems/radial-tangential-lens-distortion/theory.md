# Apply Radial and Tangential Lens Distortion

## Intuition

A pinhole model maps rays to a flat plane, but a real lens bends that mapping. Radial terms expand or shrink positions with distance from the optical center; tangential terms model a decentered lens.

## Mathematics and physical meaning

For normalized coordinates $(x,y)$, set $r^2=x^2+y^2$ and radial scale $a=1+k_1r^2+k_2r^4+k_3r^6$. Return
$$x_d=xa+2p_1xy+p_2(r^2+2x^2),$$
$$y_d=ya+p_1(r^2+2y^2)+2p_2xy.$$
All coordinates and coefficients are dimensionless. $k_1,k_2,k_3$ control radial distortion; $p_1,p_2$ control tangential distortion. Pixel intrinsics must be applied after this operation. The polynomial can cease to be physically monotone for extreme coefficients; this contract evaluates the supplied model rather than certifying a calibration.

## Visual trace

| Point | Model term | Output |
|---|---|---|
| [1,0] | k1=0.1, all others 0 | [1.1,0] |
| [1,0] | p1=0.1,p2=0.2, radial terms 0 | [1.6,0.1] |
| [0,0] | any allowed coefficients | [0,0] |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `points=[[1,0],[0,1]], coefficients=[0.1,0,0,0,0]` → `[[1.1,0],[0,1.1]]`.
2. `points=[[1,0]], coefficients=[0,0,0.1,0.2,0]` → `[[1.6,0.1]]`.

## Why this matters on a robot

Applying distortion to pixel coordinates rather than normalized rays can magnify a small calibration coefficient enormously. A wrong p1/p2 order creates direction-dependent reprojection error near the image border.

## Sources and prerequisites

- [Primary reference 1](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html)
