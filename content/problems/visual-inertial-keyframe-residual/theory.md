# Build a Visual-Inertial Residual

## Intuition

Preintegration and world-state changes use different frames and gravity conventions. Compare them in the initial body frame, then divide each residual by an uncertainty with matching units before combining visual and inertial evidence.

## Mathematics and conventions

Write $R_i,R_j$ for body-to-world rotations, $p_i,p_j$ for world positions (m), $v_i,v_j$ for world velocities (m/s), g for world gravity (m/s squared), and T for the interval (s). With gravity-free initial-body increments $\Delta R,\Delta v,\Delta p$,

$$r_R=\operatorname{Log}(\Delta R^\top R_i^\top R_j),$$
$$r_v=R_i^\top(v_j-v_i-gT)-\Delta v,$$
$$r_p=R_i^\top(p_j-p_i-v_iT-\tfrac12gT^2)-\Delta p.$$

The three residual blocks have radians, m/s and m units. Concatenate them into r and divide by the nine corresponding standard deviations. Visual residual array e has shape $(N,2)$ and pixel units; divide by its per-coordinate standard deviations too:

$$z=[r\oslash\sigma_{IMU};\operatorname{vec}_{row}(e\oslash\sigma_{visual})],\qquad E=\tfrac12z^\top z.$$

The whitened vector and cost are dimensionless. A diagonal uncertainty model is a deliberate simplification; it omits correlated IMU uncertainty and bias-state terms.

## Visual computation trace

| Stationary interval T=.1 s | World gravity term removed | Preintegrated increment | Residual |
| --- | --- | --- | --- |
| Velocity | -gT=+1 z | +1 z | 0 |
| Position | -.5gT²=+.05 z | +.05 z | 0 |
| Rotation | identity relative pose | identity | 0 |

## Worked examples

1. Identity orientations, zero positions/velocities, gravity `[0.,0.,-10.]`, T=0.1 s, delta_velocity `[0.,0.,1.]`, delta_position `[0.,0.,0.05]` and identity delta_rotation give zero IMU residual: gravity and stationary specific-force increments cancel.
2. Gravity zero, identity rotations, zero velocities/increments, positions i=`[0.,0.,0.]`, j=`[1.,0.,0.]`, T=1 s, all standard deviations 1 and visual residual `[[3.,4.]]` give rp=`[1.,0.,0.]` and cost `(1+9+16)/2=13`.

## Why this matters on a robot

Mixing body-frame increments with world-frame gravity or using the inverse rotation corrupts the factor. Overconfident visual standard deviations can dominate otherwise correct inertial evidence even when every residual is computed correctly.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1708.03852). [short-window-imu-preintegration](/problems/short-window-imu-preintegration) · [se3-exponential-logarithm](/problems/se3-exponential-logarithm)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
