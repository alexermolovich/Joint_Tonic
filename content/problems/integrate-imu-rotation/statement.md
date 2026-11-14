# Integrate IMU Rotation Increments on SO3

Implement `integrate_imu_rotation(angular_velocity, gyro_bias, durations)`.

Integrate bias-corrected body angular velocities with right-multiplied SO(3) increments.

`angular_velocity` is float64 `(N,3)` rad/s, `gyro_bias` float64 `(3,)` rad/s, both with absolute entries<=100. `durations` is float64 `(N,)` seconds, each in `[1e-6,1]`, total<=100; `0<=N<=4096`. Samples are chronological and each rate/bias describes that sample's right-handed body frame. The constant bias uses the same sensor-axis convention across the window.

Initialize DeltaR=I. For sample k compute rotation vector `(angular_velocity[k]-gyro_bias)*durations[k]`, apply the Rodrigues exponential with stable zero-angle limits, then update `DeltaR_next=DeltaR @ Exp(vector)` in that order. Return a dictionary with fresh float64 `rotations (N+1,3,3)` including initial identity, and `elapsed (N+1,)` containing zero followed by cumulative durations. Rotation k maps body-frame vectors at that state into the initial keyframe body coordinates. Empty input returns one identity and elapsed `[0.]`. No Euler-angle addition, gravity, velocity, covariance or bias estimation is included.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Angular velocity `[[0.,0.,pi/2]]`, zero gyro bias, duration `[1.]` produce initial identity followed by a 90-degree z rotation, elapsed `[0.,1.]`.
2. Angular velocities equal to the supplied gyro bias produce identity at every state. An empty window also returns identity and zero elapsed time.

## Source and scope

[Primary source](https://arxiv.org/abs/1512.02363). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
