# Depth pixels become camera-frame points

## Intuition

A pixel selects a viewing ray; depth locates a point along it. The sensor's convention matters: this exercise receives distance along the camera's forward z axis, not distance from the camera center.

## Invert the pinhole equations

Let $(u,v)$ be integer pixel column and row. Focal lengths $f_x,f_y>0$ and principal point $(c_x,c_y)$ have pixel units. The optical frame uses x right, y down, z forward. For depth z in meters, projection gives $u=f_x x/z+c_x$ and $v=f_y y/z+c_y$. Rearranging:

$$
\mathbf p_c(u,v)=z(u,v)
\begin{bmatrix}
(u-c_x)/f_x\\
(v-c_y)/f_y\\
1
\end{bmatrix}.
$$

The bracket is a dimensionless ray with last coordinate one, not a unit vector. Multiplying it by Euclidean range would overestimate off-axis z.

## Visual: image indexing becomes cloud indexing

| Image index (v,u) | Flat row v*W+u | Depth (m) | Point (m) |
|---|---:|---:|---|
| (0,0) | 0 | 1 | (0,0,1) |
| (0,1) | 1 | 2 | (1,0,2) |
| (1,0) | 2 | missing | (NaN,NaN,NaN) |
| (1,1) | 3 | 4 | (2,2,4) |

The table uses focal lengths 2 px and principal point (0,0). Reading down traverses the image row by row. The shape changes from (2,2) to (4,3) while retaining missing pixels. This trace is also the text alternative; nothing is animated.

For the final pixel, $x=(1-0)4/2=2$ m and $y=(1-0)4/2=2$ m. Its distance from the camera is $\sqrt{24}$ m, even though its depth is 4 m.

## Missing depth and calibration

Only positive finite depth is valid. Build that mask before multiplication, initialize invalid rows with three NaNs, and preserve pixel indices. Dropping rows would break correspondence with image features.

K must describe this exact image resolution. Cropping or resizing changes the principal point or focal lengths; the function cannot infer that change. Integer pixel centers avoid an unexplained half-pixel shift.

## Why this matters on a robot

Unprojection feeds obstacle maps and grasp candidates. Converting missing depth to zero creates fake points at the camera origin. Swapping row and column makes a plausible-looking cloud with incorrect geometry.

## Check your understanding

- Why retain missing rows? To keep image and point-feature indices aligned.
- Are these world coordinates? No; apply a separate calibrated rigid transform.

## Source and prerequisites

See OpenCV's [pinhole camera model](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html). First solve [projection](/problems/project-camera-points), then use [SE(3) transforms](/problems/se3-transform-points). This is an original camera-model exercise.
