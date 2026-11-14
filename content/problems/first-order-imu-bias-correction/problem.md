# Apply a First-Order Bias Correction

Implement `correct_preintegration(delta_rotation, delta_velocity, delta_position, jacobians, gyro_delta, accel_delta)`.

Apply supplied first-order bias Jacobians to an existing preintegrated measurement.

`delta_rotation` is a proper float64 `(3,3)` rotation; `delta_velocity` and `delta_position` are float64 `(3,)` in m/s and meters, expressed in the fixed initial keyframe body frame. Validate rotation with atol=1e-9, rtol=0. `jacobians` is float64 `(5,3,3)` in this order: J_R_bg, J_v_bg, J_v_ba, J_p_bg, J_p_ba. They were evaluated at the original integration bias; each maps a bias increment into the named output's units.

`gyro_delta` is float64 `(3,)` in rad/s and `accel_delta` float64 `(3,)` in m/s², each with norm<=0.01. Also require norm(J_R_bg@gyro_delta)<=0.1 radians. Return fresh `rotation = delta_rotation @ Exp(J_R_bg@gyro_delta)`, `velocity = delta_velocity+J_v_bg@gyro_delta+J_v_ba@accel_delta`, and `position = delta_position+J_p_bg@gyro_delta+J_p_ba@accel_delta`, in a dictionary. Exp is the stable SO(3) exponential and the rotation correction is right-multiplied.

Jacobians are supplied, not estimated, and their signs already encode sensitivity to the original bias. This is a first-order approximation; the magnitude bounds provide a finite teaching envelope, not an error guarantee. Large bias changes require reintegration or a separate error check. Zero deltas return independent copies.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With every Jacobian zero, any supported small bias deltas leave the original rotation, velocity and position unchanged, but return new arrays.
2. Start with identity rotation and zero velocity/position. Let J_R_bg=I, J_v_ba=2I, J_p_ba=0.5I and all other Jacobians zero. Gyro delta `[0.,0.,0.01]` and accel delta `[0.01,0.,0.]` give a local z rotation of `0.01` rad, velocity `[0.02,0.,0.]` m/s and position `[0.005,0.,0.]` meters.

## Source and scope

[Primary source](https://arxiv.org/abs/1512.02363). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
