# Preintegrate Bias-Corrected IMU Velocity and Position

Implement `preintegrate_translation(accelerations, accelerometer_bias, relative_rotations, durations)`.

Preintegrate accelerometer velocity and position increments in the initial keyframe body frame.

`accelerations` is float64 `(N,3)` specific force in m/s², `accelerometer_bias` float64 `(3,)` in m/s², with absolute entries<=100. `relative_rotations` is float64 `(N,3,3)`, each a proper rotation mapping sample k's body frame into the initial keyframe frame at the START of interval k. Validate rotations with atol=1e-9, rtol=0. `durations` is float64 `(N,)` seconds in `[1e-6,1]` with total<=100; `0<=N<=4096`.

Initialize velocity and position increments to zero. At each interval compute `force=relative_rotations[k]@(accelerations[k]-accelerometer_bias)`. Update position using the OLD velocity: `position_next=position+velocity*dt+0.5*force*dt**2`; then `velocity_next=velocity+force*dt`. Return fresh float64 `velocity (N+1,3)`, `position (N+1,3)` and `elapsed (N+1,)`, including the initial zeros, in a dictionary. Velocity and position use m/s and meters in the initial body frame.

Gravity is deliberately absent from these preintegrated quantities; it is restored when forming a world-state factor. Supplied specific force is not assumed to be zero for a stationary physical accelerometer. Rotation integration, covariance and extrinsic estimation are outside this component. Empty samples return one zero state.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One specific-force sample `[[2.,0.,0.]]`, zero bias, identity interval-start rotation, duration `[0.1]` produce final velocity `[0.2,0.,0.]` m/s and position `[0.01,0.,0.]` meters.
2. Two identical samples and durations give final velocity `[0.4,0.,0.]` m/s and position `[0.04,0.,0.]` meters. Both output traces include their initial zero row.

## Source and scope

[Primary source](https://arxiv.org/abs/1512.02363). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
