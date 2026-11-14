# Interpolate a Trajectory Between Support States

Implement `interpolate_support(start, end, duration, fractions)`.

Interpolate one constant-velocity GP support interval with fixed endpoint positions and velocities.

`start` and `end` are float64 `(D,2)`, `1<=D<=16`, columns joint position in radians and velocity in rad/s. `duration` is a Python int/float in `[1e-3,100]` seconds. `fractions` is float64 `(Q,)`, `0<=Q<=4096`, values in `[0,1]` in any order; fraction u means elapsed time u*duration. Return fresh float64 `position (Q,D)` and `velocity (Q,D)` in a dictionary, using cubic Hermite interpolation:

`q(u)=(2*u**3-3*u**2+1)*q0+(u**3-2*u**2+u)*duration*v0+(-2*u**3+3*u**2)*q1+(u**3-u**2)*duration*v1`.

Velocity is the analytic derivative with respect to elapsed seconds: differentiate in u and divide by duration. Do not wrap angles, clip results or change query order. Empty queries are supported. This cubic is the conditional mean of the independent constant-velocity, white-acceleration GP given both endpoint states. It is not interpolation for arbitrary GP kernels and does not report uncertainty, collisions or dynamic feasibility.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Start `[[0.,0.]]`, end `[[1.,0.]]`, duration `2`, fractions `[0.5]` give position `[[0.5]]` and velocity `[[0.75]]`.
2. Start `[[0.,2.]]`, end `[[4.,2.]]`, duration `2`, fractions `[0.,0.5,1.]` give positions `[[0.],[2.],[4.]]` and velocities `[[2.],[2.],[2.]]`.

## Source and scope

[Primary source](https://arxiv.org/abs/1707.07383). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
