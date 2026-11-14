# Build a Gaussian-Process Smoothness Factor

Implement `gp_motion_factor(start, end, duration, spectral_density)`.

Build one independent-joint constant-velocity Gaussian-process prior factor.

`start` and `end` are float64 `(D,2)`, `1<=D<=16`, with columns joint position in radians and velocity in rad/s. They are synchronized support states of the same rotational joints; no angle wrapping occurs. `duration` is a Python int/float in `[1e-3,100]` seconds. `spectral_density` is float64 `(D,)` in `[1e-6,1e6]`, measured in rad²/s³.

For each joint form residual `e=[q1-q0-duration*v0, v1-v0]` and covariance `Q=qc*[[duration**3/3,duration**2/2],[duration**2/2,duration]]`. Compute the lower Cholesky factor `L` with positive diagonal and the whitened residual `solve(L,e)`. Return a dictionary with fresh float64 `residual (D,2)`, `covariance (D,2,2)`, `whitened (D,2)`, and Python float `cost=0.5*sum(whitened**2)`. Covariance entries have units rad², rad²/s and rad²/s² by block; whitened residuals and cost are dimensionless. This is the independent-joint constant-velocity prior used as a GPMP2 component; it does not optimize a path or include obstacle factors.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Start and end `[[0.,0.]]`, duration `1`, spectral density `[1.]` yield residual `[[0.,0.]]`, covariance `[[[1/3,1/2],[1/2,1]]]`, whitened residual zero and cost `0`.
2. Start `[[0.,0.]]`, end `[[1.,0.]]`, duration `1`, density `[1.]` yield residual `[[1.,0.]]`, whitened `[[sqrt(3),-3]]`, and cost `6`.

## Source and scope

[Primary source](https://arxiv.org/abs/1707.07383). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
