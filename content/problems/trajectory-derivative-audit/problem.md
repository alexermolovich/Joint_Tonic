# Validate a Trajectory Against Derivative Limits

Implement `audit_derivatives(velocity, acceleration, jerk, limits)`.

Audit supplied trajectory derivative samples without claiming continuous-time feasibility.

Velocity, acceleration and jerk are float64 `(N,D)`, `0<=N<=4096`, `1<=D<=16`, in rad/s, rad/s² and rad/s³. Rows are synchronized samples at caller-declared times; the function compares supplied derivatives and does not estimate them by finite differences. `limits` is float64 `(3,D)`, rows velocity/acceleration/jerk, in matching units, with every bound at least `1e-9`. Return `violations`: fresh bool `(N,D,3)`, ordered velocity/acceleration/jerk on the last axis, True where absolute derivative is strictly greater than its bound. Return `max_ratio`: float64 `(3,D)` maximum absolute derivative divided by its limit over N (all zero for N=0), and `passed`: Python bool true iff N>0 and no violations. Equality passes; empty evidence never passes. This is a sampled audit, not a guarantee about values between samples.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One joint sample with velocity `2`, acceleration `-3`, jerk `4`, limits `[[2.],[3.],[4.]]` yields violations `[[[False,False,False]]]`, max ratios `[[1.],[1.],[1.]]`, passed True.
2. Change velocity to `2.2`: only its velocity flag is True, maximum velocity ratio is `1.1`, and passed is False.

## Source and scope

[Primary source](https://arxiv.org/abs/2105.04830). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
