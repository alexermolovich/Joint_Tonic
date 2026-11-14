# Validate Missing-Modality and Stale-Sensor Inputs

A tensor with the right shape may still describe the robot’s past. Presence and freshness are separate facts, and a policy should specify which sensors are essential before deciding whether to issue an action.

## Contract

`sensor_readiness(present,timestamps,now,max_age,required)` takes present:bool(B,M),1<=B<=64,1<=M<=32; timestamps:real(B,M) seconds>=0; now:real(B,) seconds>=0; max_age:real(M,) seconds>=0; required:bool(M,). Return dict usable:bool(B,M), stale:bool(B,M), ready:bool(B,). A present sensor is stale when timestamp>now or now-timestamp>max_age. Missing sensors have stale=False and usable=False. usable=present&~stale. A row is ready iff every required sensor is usable; if none required, ready=True even with no present sensor. Validate all timestamps including missing entries.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

All timestamps and ages are seconds on one synchronized clock; sensors retain caller-declared calibration/frame. Boundary age=max_age is usable; future sensor stamps are not usable. No clock correction is performed. Original deployment input gate motivated by embodied multimodal models. It does not impute a missing modality or establish spatial calibration validity.


## Example 1

present=[[True,True]], timestamps=[[9,8]], now=[10], max_age=[1,1], required=[True,True] returns usable=[[True,False]], stale=[[False,True]], ready=[False].

## Example 2

present=[[False,True]], timestamps=[[0,11]], now=[10], max_age=[1,1], required=[False,False] returns usable=[[False,False]], stale=[[False,True]], ready=[True]. No required sensors is a deliberate vacuous gate, not proof of useful perception.
