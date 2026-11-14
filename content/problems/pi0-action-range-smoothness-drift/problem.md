# Monitor Continuous-Action Range and Smoothness Drift

An action can stay inside its allowed range yet jump too quickly between control ticks. Track range and finite-difference speed separately, then count their union so a single bad sample does not contribute twice to the drift rate.

## Contract

actions real(T,D),1<=T<=4096,1<=D<=32 in normalized controller coordinates; timestamps real(T,) seconds nonnegative strictly increasing; lower/upper/max_speed real(D,), lower<=upper,max_speed>=0; baseline_rate real(D,) in[0,1], historical fraction of flagged time rows per channel. Range flag when a<lower OR a>upper (equality accepted); speed flag at t>0 when abs(a[t]-a[t-1])/(timestamp[t]-timestamp[t-1])>max_speed, row0alwaysFalse. Union flags across range/speed perchannel. Return range_violation/speed_violation bool(T,D), rate float64(D,)=mean(union,axis0) over ALLT including row0, drift=rate-baseline_rate. Do not alter or clip actions; one-stepT=1 has zero speed flags.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized action units; timestamps seconds; max_speed normalized action units per second. Inputs must use the same normalization and controller frame as the baseline. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.


## Example 1

actions=[[0],[2],[2]],times=[0,1,2],bounds[0]..[1],speed[1],baseline[.5] returns range[False,True,True],speed[False,True,False],rate[2/3],drift[1/6].

## Example 2

actions=[[1]],time=[5],bounds[0]..[1],speed[0],baseline[0] has no flags and rate/drift0: the upper bound is inclusive.
