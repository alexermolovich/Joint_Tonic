# Build a Visual-Inertial Residual

Implement `keyframe_residual(rotations, positions, velocities, gravity, duration, delta_rotation, delta_velocity, delta_position, imu_std, visual_residuals, visual_std)`.

Combine a keyframe IMU residual with already computed visual residuals using declared diagonal uncertainties.

`rotations (2,3,3)` are proper float64 body-to-world rotations at keyframes i,j. `positions (2,3)` and `velocities (2,3)` are world-frame meters and m/s. `gravity (3,)` is world-frame m/s squared, absolute entries <=100. `duration` is a Python int/float in `[1e-6,100]` seconds. `delta_rotation (3,3)` is proper, and `delta_velocity (3,)`, `delta_position (3,)` are preintegrated increments in the initial body frame, in m/s and m.

`imu_std (9,)` is float64 in `[1e-6,1000]`, ordered rotation (radians), velocity (m/s), position (m). `visual_residuals (N,2)` and `visual_std (N,2)` are float64 pixel quantities, `0<=N<=16384`, std entries in `[1e-6,1000]`. Visual residuals are supplied measured-minus-projected pixels; projection is outside this function.

Compute rR=Log(delta_rotation.T@Ri.T@Rj), the principal SO(3) rotation vector, requiring its angle <=pi-1e-4. Compute rv=Ri.T@(vj-vi-gravity*T)-delta_velocity, and rp=Ri.T@(pj-pi-vi*T-0.5*gravity*T^2)-delta_position. Return `inertial (9,)` ordered rR,rv,rp; `whitened (9+2N,)` comprising inertial/imu_std followed by flattened visual_residuals/visual_std in row-major order; and Python float `cost=0.5*dot(whitened,whitened)`.

All proper rotations use atol=1e-9, rtol=0 validation. This is a diagonal-noise teaching factor without bias-state residuals, full covariance whitening, robust visual loss or optimization. Do not add gravity to the supplied preintegrated increments.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity orientations, zero positions/velocities, gravity `[0.,0.,-10.]`, T=0.1 s, delta_velocity `[0.,0.,1.]`, delta_position `[0.,0.,0.05]` and identity delta_rotation give zero IMU residual: gravity and stationary specific-force increments cancel.
2. Gravity zero, identity rotations, zero velocities/increments, positions i=`[0.,0.,0.]`, j=`[1.,0.,0.]`, T=1 s, all standard deviations 1 and visual residual `[[3.,4.]]` give rp=`[1.,0.,0.]` and cost `(1+9+16)/2=13`.

## Source and scope

[Primary source](https://arxiv.org/abs/1708.03852). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
