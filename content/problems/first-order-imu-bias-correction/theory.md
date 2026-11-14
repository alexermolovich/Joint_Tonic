# Apply a First-Order Bias Correction

## Intuition

When a small bias estimate changes, its stored Jacobians predict how the preintegrated measurement changes. Rotation must remain on SO(3); its correction is composed as a small rotation rather than added to matrix entries.

## Mathematics and conventions

For gyro and accelerometer bias increments $\delta b_g,\delta b_a$, use the supplied sensitivities:

$$\Delta R'=\Delta R\operatorname{Exp}(J_{R,g}\delta b_g),$$
$$\Delta v'=\Delta v+J_{v,g}\delta b_g+J_{v,a}\delta b_a,\qquad\Delta p'=\Delta p+J_{p,g}\delta b_g+J_{p,a}\delta b_a.$$

Each Jacobian has output units divided by its bias-input units. Thus $J_{R,g}\delta b_g$ is radians, velocity corrections m/s, and position corrections meters. The rotation tangent is local to the final preintegrated orientation, which determines the right-composition order.

## Visual computation trace

| Correction block | Input | Output contribution |
| --- | --- | --- |
| J_R_bg=I | gyro delta .01 about z | local z rotation .01 rad |
| J_v_ba=2I | accel delta .01 along x | velocity +.02 m/s |
| J_p_ba=.5I | same accel delta | position +.005 m |

## Worked examples

1. With every Jacobian zero, any supported small bias deltas leave the original rotation, velocity and position unchanged, but return new arrays.
2. Start with identity rotation and zero velocity/position. Let J_R_bg=I, J_v_ba=2I, J_p_ba=0.5I and all other Jacobians zero. Gyro delta `[0.,0.,0.01]` and accel delta `[0.01,0.,0.]` give a local z rotation of `0.01` rad, velocity `[0.02,0.,0.]` m/s and position `[0.005,0.,0.]` meters.

## Why this matters on a robot

Flipping the rotation composition side can be invisible near identity but wrong after a large turn. Reusing Jacobians far from their bias linearization point can also produce an inaccurate correction despite valid shapes.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1512.02363). [integrate-imu-rotation](/problems/integrate-imu-rotation) · [preintegrate-imu-translation](/problems/preintegrate-imu-translation)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
