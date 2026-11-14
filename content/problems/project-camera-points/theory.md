# Perspective is a ratio

## Intuition

Double a point's lateral distance while holding depth fixed and it moves twice as far from the image center. Double its depth while holding lateral distance fixed and the image displacement halves. A pinhole camera captures these ratios.

## Geometry and mathematics

A camera-frame point is $p=(x,y,z)$ in meters, with z forward. The focal lengths $f_x,f_y$ and principal point $(c_x,c_y)$ are in pixels. Projection is

$$
u=f_x\frac{x}{z}+c_x,\qquad v=f_y\frac{y}{z}+c_y.
$$

The ratios $x/z$ and $y/z$ are dimensionless. The focal lengths convert them to pixel displacement, and the principal point shifts from the optical axis to image coordinates. We assume an ideal zero-skew, distortion-free camera:

$$
K=\begin{bmatrix}f_x&0&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}.
$$

The function returns three aligned arrays: `(N,2)` pixels, `(N,)` depth, and `(N,)` validity. No point is discarded, so a later component can still associate every row with its original sensor measurement.

## Visual walkthrough

The projection view connects a point and camera origin with a ray, then marks the corresponding position on the image plane. A depth control demonstrates the inverse-distance relationship. The accompanying table records x/y/z, u/v, and the reason a point is invalid.

| State | Pixel value | Validity |
|---|---|---|
| `z <= 1e-8` | both NaN | false |
| sufficient depth, outside image | calculated coordinates | false |
| sufficient depth, inside image | calculated coordinates | true |

## Worked numbers

Take $f_x=100,f_y=80,c_x=50,c_y=30$ and $(x,y,z)=(0.2,-0.5,2)$. Then $u=100(0.2/2)+50=60$ and $v=80(-0.5/2)+30=10$. In a 100x60 image, `(60,10)` is valid. The same point at z=1 moves to `(70,-10)` and is above the image.

## Why this matters on a robot

Camera projection connects a geometric grasp candidate to an image crop or semantic label. Returning an outside coordinate as “valid” can make a downstream crop select unrelated pixels; treating a negative-depth point as visible can select an obstacle behind the camera. Version the calibration, image dimensions, resize/crop transform, and frame convention together.

## Common failures

- Dividing before masking creates infinity or warnings at zero depth.
- Clipping projected pixels into the image makes an outside point appear valid. This task keeps the original projected coordinates instead.
- Swapping `(width,height)` with array shape `(height,width)` rotates the validity logic.
- Using `<=width` permits an invalid array index at the right boundary.

## Sources and scope

The [official OpenCV calibration documentation](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) describes the pinhole model and later distortion extensions. This exercise intentionally excludes distortion, extrinsics, rolling shutter, and occlusion. Its examples and explanation are original.
