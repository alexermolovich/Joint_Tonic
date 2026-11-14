# Pull Back a Local Motion Metric

Implement `pullback_policy(jacobian, jacobian_rate, joint_velocity, task_metric, task_force)`.

Pull one supplied natural-form task policy into normalized joint coordinates.

`jacobian` and `jacobian_rate` are float64 `(T,D)`, `1<=T,D<=16`. `joint_velocity` is `(D,)`, `task_metric` `(T,T)`, and `task_force` `(T,)`. Joint and task coordinates are normalized dimensionless coordinates with a fixed caller-defined scaling; J is dimensionless, its time derivative Jdot is 1/s, velocity is 1/s, and natural force is 1/s². The metric is dimensionless. All inputs describe one synchronized state; the force is a supplied natural-form policy value, not a physical Newton force.

Validate M against its transpose with atol=1e-10, rtol=0, then symmetrize. Compute its eigenvalues; reject any less than -1e-10, clip accepted negative eigenvalues to zero, and reconstruct the effective metric. This numerical PSD normalization is part of the contract. Return fresh float64 `metric (D,D) = J.T @ M @ J` and `force (D,) = J.T @ (f - M @ Jdot @ joint_velocity)` in a dictionary. Do not omit the curvature correction, invert a metric or generate leaf policies. An exactly zero task metric is allowed; task_force remains an independent supplied input.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. J=`[[2.]]`, Jdot=`[[1.]]`, joint velocity `[3.]`, metric `[[4.]]`, force `[20.]` give pulled metric `[[16.]]` and force `[16.]`: subtract the task curvature contribution `4*1*3=12` before multiplying by J.T.
2. With the same inputs but Jdot=`[[0.]]`, pulled metric remains `[[16.]]`, while force becomes `[40.]`.

## Source and scope

[Primary source](https://arxiv.org/abs/1811.07049). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
