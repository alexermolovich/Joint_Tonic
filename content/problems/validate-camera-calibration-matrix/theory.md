# Validate a Camera Calibration Matrix

## Intuition

A calibration matrix can be the right shape yet belong to the wrong image resolution or use an invalid homogeneous scale. Validate the contract before projecting a scene.

## Mathematics and physical meaning

The pinhole intrinsic form is
$$K=\begin{bmatrix}f_x&s&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}.$$
$f_x,f_y>0$ are focal lengths in pixels, $s$ is skew, and $(c_x,c_y)$ is the principal point. For image width $W$ and height $H$, this exercise’s deployment policy requires $0\le c_x<W$ and $0\le c_y<H$. Some physical cameras can calibrate to an off-image principal point; rejecting that is an explicit policy of this task, not a universal theorem about cameras.

## Visual trace

| Field for 640×480 image | Example | Policy |
|---|---|---|
| fx,fy | 500,510 | positive |
| cx,cy | 320,240 | inside image |
| bottom row | [0,0,1] | homogeneous form |
| cx after wrong resize metadata | 640 | outside -> false |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `K=[[500,0,320],[0,510,240],[0,0,1]], width=640, height=480` → `True`.
2. Same K with width=320 → `False` because cx equals the excluded right boundary.

## Why this matters on a robot

A matrix calibrated before image resizing may pass numerical checks but project incorrectly after resizing. Pair intrinsics with resolution and calibration version; this validator cannot assess reprojection accuracy from K alone.

## Sources and prerequisites

- [Primary reference 1](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html)
