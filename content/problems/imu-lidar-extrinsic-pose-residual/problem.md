# Assemble an IMU-Lidar Pose Constraint

Implement `imu_lidar_residual(world_from_imu, imu_from_lidar, lidar_relative, std)`.

`imu_lidar_residual(world_from_imu, imu_from_lidar, lidar_relative, std)` world_from_imu(2,4,4),shared extrinsic(4,4),lidar_relative(4,4) maps lidar-j into lidar-i;std(6)in[1e-6,1000], translation meters thenrotation radians.

Predicted lidar relative=(Ti Til)^-1(Tj Til). E=lidar_relative^-1 predicted.

Return predicted(4,4),translation=E[:3,3](3),rotation=Log(E.R)(3),whitened(6)=concattranslation,rotation/std,cost half norm².

Requireprincipal rotation error<=pi−1e-4.

Translation is in measured residual frame; split translation/rotation residual is explicitly NOT full SE(3) log translational Jacobian or complete LIO-SAM IMU velocity/bias factor.

Example: extrinsic I,posesI andtranslationx2,measuredtranslationx1,std1=>translation[1,0,0],rotation0,cost.5.

Example: pure IMU Rz90 with lidar lever arm[1,0,0]=>predictedRz90,translation[-1,1,0],matching measurement gives zero.

Known extrinsics are essential.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity extrinsic, IMU world poses at x=0 and x=2, measured lidar relative translation x=1, and all standard deviations 1 give translation residual [1,0,0], zero rotation residual, and cost 0.5.
2. The IMU rotates 90 degrees about z at a fixed origin. A lidar mounted one meter along IMU x has relative rotation Rz90 and relative translation [-1,1,0].

Supplying exactly that measurement gives zero cost.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.00258).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
