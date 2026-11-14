# Route Inputs Through a Dual-System Policy Interface

A semantic model and a motor model need different inputs and may run at different rates. Preserve the semantic features, project state using the robot-specific interface, and report whether the cached context is fresh enough for the current observation.

## Contract

context real(B,C), state real(B,S),1<=B<=64,1<=C,S<=64; embodiment_ids integer(B,), state_projectors real(G,S,E),1<=G<=16,1<=E<=64, IDs0..G-1. context_time/observation_time real(B,) seconds>=0; max_context_age real scalar0..1e6 seconds. Project each state row using its embodiment-specific matrix and concatenate unchanged context then projected state: conditioning float64(B,C+E). Return conditioning, head_ids int64(B,) copy of embodiment_ids, ready bool(B,), context_age float64(B,)=observation-context time. Ready iff0<=age<=max_context_age. Future/stale context is reported not raised; conditioning is still returned for inspection and must NOT be executed when readyFalse. This routes already encoded features; no asynchronous runtime, model inference or implicit context refresh.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates. Physical timestamps and maximum context age are seconds on one synchronized monotonic clock; no cross-device clock correction. Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.


## Example 1

context=[[5]],state=[[2]],IDs=[0],projectors=[[[3]]],context_time=[1],observation_time=[1.2],max_age=.5 returns conditioning[[5,6]],head_ids[0],age[.2],ready[True].

## Example 2

Same features with context_time=[2],observation_time=[1] returns age[-1],ready[False], while keeping conditioning[[5,6]] for inspection.
