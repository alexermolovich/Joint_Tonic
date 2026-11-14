# Measure Closed-Loop Latency and Action Dropouts

An inference that finishes after its control deadline is not equivalent to an action applied on time. Keep missing commands separate from delivered-but-late commands while reporting their combined effect on the loop.

## Contract

`control_latency_report(observed_ms, applied_ms, deadline_ms)` receives equal nonempty vectors(T,), T<=10000, observation timestamps>=0 strictly increasing and applied timestamps either -1 (missing action) or >=their observation. Different applied timestamps need not increase. deadline_ms is a positive scalar<=1e6. Return dict latency_ms:float64(T,) using -1 for missing, dropout_rate:float, deadline_miss_rate:float, mean_latency_ms:float or None. Dropout is missing; deadline miss is missing OR latency>deadline. Both rates divide by T. Mean uses delivered actions only, None if none.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

All times and deadline are milliseconds on one synchronized monotonic clock; rates dimensionless. Each applied entry corresponds to exactly its observed entry; no timestamp matching is inferred. Original measurement exercise motivated by RT-1 control-time efficiency; no proprietary robot telemetry or published latency number is reproduced.


## Example 1

observed_ms=[0,10,20], applied_ms=[5,-1,35], deadline_ms=10 returns latency_ms=[5,-1,15], dropout_rate=1/3, deadline_miss_rate=2/3 and mean_latency_ms=10.

## Example 2

observed_ms=[2], applied_ms=[-1], deadline_ms=4 returns latency_ms=[-1], both rates1 and mean_latency_ms=None.
