# Propagate Preintegration Covariance

Implement `preintegration_covariance(rotation_vectors, specific_force, durations, noise_variance)`.

`preintegration_covariance(rotation_vectors, specific_force, durations, noise_variance)` rotation_vectors (N,3) body-frame integrated angular increments radians, norm<=3; force(N,3) bias-corrected body specific force m/s² abs<=100;dt(N)seconds[1e-6,1],sum<=100,N0..1024;noise_variance (N,6) in[0,100], per-sample discrete variances of gyroscope(rad/s) then accelerometer(m/s²), NOT continuous spectral densities.

Start rotation R=I,cov P=zeros9.

State error order(theta radians,velocity m/s,position m), theta right-local current-body, velocity/position initial body.

For each old R and h=dt, phi=rotvec, E=Exp(phi), right Jacobian Jr=I−(1−cosθ)/θ²[phi]x+(θ−sinθ)/θ³[phi]x² with analytic small-angle continuation. A block rows [[E.T,0,0],[-R[f]x h,I,0],[-.5R[f]x h²,I h,I]]. B block rows [[Jr h,0],[0,R h],[0,.5R h²]]. P'=A P A.T+B diag(q) B.T, symmetrize roundoff; R'=R E.

Return covariance(N+1,9,9) and final_rotation(3,3).

This reproduces the nine-state first-order noise recurrence with supplied increments, fixed biases, and diagonal discrete sensor noise; no bias random walk or continuous-noise discretization.

Example: one zero-rotation/force step h1,gyro variances 1,accelerometer variances 4=>diagonal orientation variances 1,diagonal velocity variances 4,diagonal position variances 1 and each matching v/p covariance2.

Example: N=0=>single zero 9×9 matrix,R identity.

Independent oracle propagates noise impulse columns through the error recurrence before forming their Gram matrix.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One sample has zero rotation and force, duration 1 second, gyro variances [1,1,1] and accelerometer variances [4,4,4].

Final orientation-error variances are 1, velocity variances 4, position variances 1, and matching velocity/position cross-covariances 2.
2. Empty sample arrays return covariance shape (1,9,9) containing zeros and final rotation equal to identity.

## Source and scope

[Primary source](https://arxiv.org/abs/1512.02363).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
