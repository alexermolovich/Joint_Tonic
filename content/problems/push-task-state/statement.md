# Push Robot State into a Task Space

Implement `push_task_state(task_position, jacobian, joint_velocity)`.

Push a synchronized joint velocity through a supplied task Jacobian.

`task_position` is float64 `(T,)` meters, `1<=T<=16`. `jacobian` is float64 `(T,D)` meters/radian, `1<=D<=16`. `joint_velocity` is float64 `(D,)` radians/second. The caller has evaluated the task map and Jacobian at the same joint configuration and time; task axes retain that map's ordering in its declared frame. Return a dictionary containing fresh float64 `position (T,)`, a copy of task_position, and `velocity (T,) = jacobian @ joint_velocity` in meters/second. This is one RMP pushforward operation; no forward kinematics, finite-difference Jacobian, automatic differentiation or acceleration calculation is requested.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Position `[3.,4.]`, Jacobian `[[1.,2.],[0.,1.]]`, joint velocity `[2.,-1.]` give position `[3.,4.]` and task velocity `[0.,-1.]` m/s.
2. Position `[1.]`, Jacobian `[[2.,3.]]`, joint velocity `[0.,0.]` give position `[1.]` and velocity `[0.]`, both in fresh arrays.

## Source and scope

[Primary source](https://arxiv.org/abs/1811.07049). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
