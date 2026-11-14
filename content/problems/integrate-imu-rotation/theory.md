# Integrate IMU Rotation Increments on SO3

## Intuition

Rotations accumulate by composition, not by adding angle coordinates. The body frame changes after every increment, so multiplying on the wrong side changes the integrated orientation when rotations do not commute.

## Mathematics and conventions

For angular velocity $\omega_k$ and constant sensor bias $b_g$ in rad/s, interval $\Delta t_k$ in seconds, define

$$\phi_k=(\omega_k-b_g)\Delta t_k,\qquad\Delta R_0=I,\qquad\Delta R_{k+1}=\Delta R_k\operatorname{Exp}(\phi_k).$$

Each matrix maps the current body frame into the fixed initial keyframe body frame. Its columns describe current body axes in that initial frame. Elapsed time is $\tau_{k+1}=\tau_k+\Delta t_k$. The gyro bias is subtracted before multiplication by time; adding rotations as Euler angles is a different operation.

## Visual computation trace

| Step | Body increment | Accumulated orientation |
| --- | --- | --- |
| Start | none | identity |
| 1 | rotation about body x | Rx |
| 2 | rotation about new body y | Rx Ry, not Ry Rx |

## Worked examples

1. Angular velocity `[[0.,0.,pi/2]]`, zero gyro bias, duration `[1.]` produce initial identity followed by a 90-degree z rotation, elapsed `[0.,1.]`.
2. Angular velocities equal to the supplied gyro bias produce identity at every state. An empty window also returns identity and zero elapsed time.

## Why this matters on a robot

A wrong multiplication order can remain hidden during single-axis motion. Clock errors and gyro bias cause drift even when every resulting matrix is orthogonal.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1512.02363). [se3-exponential-logarithm](/problems/se3-exponential-logarithm)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
