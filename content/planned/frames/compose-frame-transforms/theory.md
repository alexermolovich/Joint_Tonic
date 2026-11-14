# Compose coordinates without losing their frames

## Intuition

A camera mount offset is measured in the robot base frame. When the base rotates, that offset rotates in the world too. Simply adding the two translations ignores the orientation of the first frame.

## Frame cancellation

Let $T_{ab}$ mean a-from-b and $T_{bc}$ mean b-from-c. All frames are right-handed and all translations are meters at the same timestamp. A homogeneous column point obeys $\bar{\mathbf p}_a=T_{ab}\bar{\mathbf p}_b$. Substitution gives

$$
T_{ac}=T_{ab}T_{bc}
=\begin{bmatrix}
R_{ab}R_{bc}&R_{ab}\mathbf t_{bc}+\mathbf t_{ab}\\
\mathbf0^\top&1
\end{bmatrix}.
$$

Each $R$ is a dimensionless 3×3 proper rotation; each $\mathbf t$ is a 3-vector. Adjacent b labels cancel. Reversing the matrix order usually expresses no meaningful chain under these labels.

To return to frame c, solve $\mathbf p_a=R_{ac}\mathbf p_c+\mathbf t_{ac}$:

$$
T_{ca}=\begin{bmatrix}
R_{ac}^{\top}&-R_{ac}^{\top}\mathbf t_{ac}\\
\mathbf0^\top&1
\end{bmatrix}.
$$

The inverse translation must also change frame; negating it alone is incorrect whenever rotation is present.

## Visual: follow the camera origin

| Stage | Coordinates | Units | Explanation |
|---|---|---|---|
| Camera origin in camera | (0,0,0) | m | Start |
| Apply base-from-camera | (1,0,0) | m | Mount lies along base x |
| Rotate into world | (0,1,0) | m | Base is turned +90° about z |
| Add world base position | (1,1,0) | m | Base origin is (1,0,0) |

This static frame trace is also a text alternative. The final point equals the translation column of T_ac. Applying the inverse rotation then translation returns it to (0,0,0).

## Validate meaning as well as shape

A 4×4 array may encode scaling or reflection, not a robot pose. Require $R^\top R=I$ and $\det R=1$. The labels, meters and exact measurement timestamp are part of the same contract. This exercise rejects asynchronous records instead of silently mixing poses.

## Why this matters on a robot

Wrong composition order can put a grasp beside the object even when every matrix looks reasonable. Millimeters treated as meters create a thousand-fold offset. Recording frame names, calibration version and measurement time helps detect these mistakes upstream.

## Check your understanding

- Is t_bc expressed in world coordinates? No, it is expressed in b.
- Is a general inverse required? No, orthonormal rotations invert by transpose.

## Source and prerequisite

Read the [Modern Robotics transform explanation](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/), then compare with [transforming points](/problems/se3-transform-points). The records and validation policy here are original.
