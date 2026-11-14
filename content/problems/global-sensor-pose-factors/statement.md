# Assemble Sensor-Specific Pose Factors

Implement `global_factors(world_from_body, body_from_sensor, gps, magnetic, world_field, height, std, valid)`.

`global_factors(world_from_body, body_from_sensor, gps, magnetic, world_field, height, std, valid)` transforms(N,4,4) and shared(4,4),0<=N<=4096.

Sensor offset/rotation known; one collocated GPS/magnetometer/barometer frame is a teaching restriction.

GPS(N,3) world ENU meters, magnetic(N,3) sensor-frame field vector in microtesla, world_field(3) ENU same units.

Require each magnetic norm and world_field norm>1e-9 including masked rows.

Height(N) is sensor altitude meters in same ENU datum (pressure conversion already done). std (N,7) in[1e-6,1000], ordered3 GPS meters,3 unit-direction dimensionless,1 height meters; valid(N,3) GPS/magnetic/barometer availability.

Predicted sensor pose Ts=Tb Tbs.

Residual signs measured-minus-predicted: gps-p_s, magnetic/norm−R_s.T(world_field/norm), height-p_s,z.

Return raw(N,7),whitened(N,7),cost Python float .5sum(whitened²); unavailable entire sensor block zero, all supplied values still validated.

Whitening uses diagonal std, not full covariance.

No calibrated field magnitude heuristic or bias estimation.

Example all identity, gps[1,2,3],mag[1,0,0],world field[1,0,0],height4,std1,all valid=>raw[1,2,3,0,0,0,4],cost15.

Example: body identity, sensor offset[1,0,0],sensor rotationRz90, gps[1,0,0],mag[0,-2,0],field[5,0,0],height0=>all zero.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Body and sensor transforms are identity.

GPS [1,2,3], magnetic [1,0,0], world field [1,0,0], height 4, all standard deviations 1 and all sensors available give raw [1,2,3,0,0,0,4] and cost 15.
2. The body is identity; the sensor has translation [1,0,0] and a 90-degree z rotation.

GPS [1,0,0], sensor magnetic [0,-2,0], world field [5,0,0], and height 0 give zero residuals.

## Source and scope

[Primary source](https://arxiv.org/abs/1901.03642).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
