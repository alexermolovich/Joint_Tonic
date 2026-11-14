# Integrate a Constant-Jerk Motion Segment

Implement `integrate_jerk(position, velocity, acceleration, jerk, duration)`.

Integrate one constant-jerk segment for several rotational joints.

The four float64 arrays have shape `(D,)`, `1<=D<=64`: position is radians, velocity radians/second, acceleration radians/second², and jerk radians/second³. All joint axes are independent coordinates of the same robot; no spatial transform occurs. `duration` is a Python int/float in `[0,100]` seconds, measured from the supplied common start time. Return a dict of fresh float64 `(D,)` arrays: `position=q+v*t+a*t²/2+j*t³/6`, `velocity=v+a*t+j*t²/2`, `acceleration=a+j*t`. Duration zero returns independent copies of the initial state. This integrates a supplied segment; it does not choose switching times, enforce joint limits, or implement Ruckig's time-optimal search.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Initial `q=v=a=[0.]`, jerk `[2.]`, duration `0.5` gives position `[1/24]`, velocity `[0.25]`, acceleration `[1.]` in the stated units.
2. Initial `q=[1.]`, `v=[2.]`, `a=[3.]`, jerk `[4.]`, duration `0` returns `[1.]`, `[2.]`, `[3.]` in fresh arrays.

## Source and scope

[Primary source](https://arxiv.org/abs/2105.04830). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
