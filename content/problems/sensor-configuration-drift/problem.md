# Compare Drift Across Sensor Configurations

Implement `compare_drift(estimated, reference, valid, baseline)`.

`compare_drift(estimated, reference, valid, baseline)` estimated(C,N,3),1<=C<=64,1<=N<=8192,C*N<=262144; reference(N,3),valid(C,N), baseline built-in int0..C-1.

Positions meters, already same world frame and matched timestamps.

Use ONLY common evidence common=all(valid,axis0) for every configuration.

Return common(N),count int,errors(C,N) with NaN outsidecommon,rmse(C),endpoint(C),improvement(C),best int.

Errors Euclidean position norm; RMSE=sqrt(mean(errors²)); endpoint uses highest common sample index, not arbitrary last valid per configuration; improvement=baseline_rmse - rmse inmeters.

Best minRMSE first-index ties; if no common count 0,all metrics NaN,best -1.

No posthoc alignment, interpolation, or assertion that better absolute error is solely less accumulated drift.

Example: reference[[0,0,0],[1,0,0]], estimated0=reference,estimated1=reference+[1,0,0],all valid,baseline1=>rmse[0,1],endpoint[0,1],improvement[1,0],best0.

Example: valid[[True,False],[False,True]]=>no common.

Comparison intentionally sacrifices coverage to prevent missing-data advantages.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Reference positions are [[0,0,0],[1,0,0]].

Configuration 0 equals reference; configuration 1 adds [1,0,0] at both times.

With all entries valid and baseline 1, RMSE and endpoint errors are [0,1] meters, improvement [1,0], and best index 0.
2. Valid masks [[True,False],[False,True]] have no common sample.

Count is 0, best is -1, and every error/aggregate is NaN.

## Source and scope

[Primary source](https://arxiv.org/abs/1901.03642).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
