# One point, two coordinate descriptions

## Intuition

A physical point does not move when you change its coordinate frame. Its three numbers change because the frame's origin and basis axes change. Here `T` tells us where the camera's origin and axes lie in the world. First express a camera-frame displacement along those world-space axes; then add the world-space camera origin.

## Frame and tensor contract

Write $R_{wc}\in\mathbb R^{3\times3}$ for the camera-to-world rotation and $t_{wc}\in\mathbb R^3$ for the world position of the camera origin. The subscript `wc` means **world from camera**. Points and translations are in meters; rotation coefficients are dimensionless.

For a column-vector point $p_c$, the defining relation is

$$
p_w = R_{wc}p_c+t_{wc}.
$$

The homogeneous representation packages both operations:

$$
T_{wc}=\begin{bmatrix}R_{wc}&t_{wc}\\0&1\end{bmatrix},\qquad
\begin{bmatrix}p_w\\1\end{bmatrix}=T_{wc}\begin{bmatrix}p_c\\1\end{bmatrix}.
$$

Our batch stores points as **rows**, so `(N,3) @ (3,3)` becomes `points @ R.T`. Adding a `(3,)` translation broadcasts across N rows. The single-point shape `(3,)` follows the same expression and remains one-dimensional.

## Visual walkthrough

In the transform view, the red, green, and blue camera axes show the columns of $R_{wc}$. The arrow from the world origin to the camera origin shows $t_{wc}$. Selecting a point highlights its three camera-axis contributions and their world-space sum. The coordinate table supplies the same values without needing a 3D view.

| Quantity | Camera representation | World representation |
|---|---|---|
| Camera origin | `(0,0,0)` | `t_wc` |
| One-meter camera x displacement | `(1,0,0)` | first column of `R_wc` |
| Arbitrary point | `p_c` | `R_wc @ p_c + t_wc` |

## Worked numbers

For a 90-degree rotation around world z, take $R_{wc}=[[0,-1,0],[1,0,0],[0,0,1]]$. With $p_c=(2,1,0)$, rotation gives $(-1,2,0)$. Adding $t_{wc}=(1,2,3)$ yields $p_w=(0,4,3)$.

## Why validate the rotation?

A rigid rotation preserves lengths and orientation. It satisfies

$$
R^\top R=I,\qquad\det(R)=1.
$$

A matrix with determinant -1 reflects the robot scene; a matrix with scaled columns changes distances. Neither is an SE(3) transform even if the shape is correct.

## Why this matters on a robot

A mistaken transform direction can place a target behind a camera or beyond a gripper's workspace. Store calibration version, frame names, and timestamps alongside observations. In a live system the transform may change over time; this exercise deliberately assumes one static synchronized transform.

## Common failures

- Adding translation before rotation changes its frame.
- Using `R` rather than `R.T` for row-batched points rotates in the opposite direction.
- Inverting a transform that is already camera-to-world reverses the requested mapping.
- Returning the input unchanged for identity can accidentally share storage.

## Further reading

[Modern Robotics: homogeneous transformation matrices](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/) describes the underlying frame convention. This page and its examples are original teaching material.
