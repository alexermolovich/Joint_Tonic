# Validate a Visual-Inertial Initialization

Implement `validate_initialization(scale, gravity, gyro_bias, accel_bias, residuals, valid, jacobian, limits)`.

`validate_initialization(scale, gravity, gyro_bias, accel_bias, residuals, valid, jacobian, limits)` scale builtinfloat/int[1e-6,1e3];gravity3world m/s²,gyro_bias (3,)rad/s,accel_bias (3,)m/s²;residuals(R)already whitened dimensionless,valid(R)bool,R0..4096;jacobian(R,D)dimensionless whitened/scaled gauge-fixed,1<=D<=32,abs<=1000;limits(7)floats = [min_scale,max_scale,gravity_tolerance,max_gyro_norm,max_accel_norm,max_rms,relative_rank_cutoff], scale interval within[1e-6,1e3]ordered, other thresholds[0,1000], cutoff[1e-12,.01].

Eligible rowsvalid determine RMS and SVD rank with strict cutoff sigma>cut*sigma_max.

Return count int,rank int,rms float(NaN if none),gravity_error float abs(normgravity−9.81),checks bool(6) ordered [at least D valid rows AND rank D, minscale<=scale<=maxscale, gravity error<=tol, gyro norm<=max,accelerometer norm<=max,RMS <=max],acceptedbool(allchecks).

No-evidence RMS check is False.

Original inspectable diagnostic over supplied initialization candidate, not optimizer, ORB-SLAM3 exact acceptanceheuristic, or nonlinearobservability proof.

Gravity directionnotgated: estimateisworld frame and only magnitude check.

Example: D=1,R1,J[[1]],residual[.2],validTrue,scale1,g[0,0,-9.81],biases0,limits[.5,2,.1,.1,.1,.2,1e-6]=>all True,rms.2,rank1.

Example: two identical J rows[[1,0],[1,0]],residual0=>rank1,first False,reject even a perfect fit.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Scale 1, gravity [0,0,-9.81], zero biases, residual [0.2], valid [True], Jacobian [[1]], and limits [0.5,2,0.1,0.1,0.1,0.2,1e-6] pass all six checks.

Rank is 1 and RMS is 0.2.
2. Jacobian rows [[1,0],[1,0]] have rank 1 despite two observations and zero residuals.

The observability check fails, so the candidate is rejected even with a perfect residual fit.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.11898).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
