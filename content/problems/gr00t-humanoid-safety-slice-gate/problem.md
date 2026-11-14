# Gate a Humanoid Policy Release on Safety Slices

A release decision needs evidence for every required scenario, not just a good overall score. Require enough trials, no recorded safety incidents, adequate success and acceptable latency while retaining optional failures for inspection.

## Contract

Integer vectors trials,successes,safety_incidents(S,),1<=S<=128,0<=successes,incidents<=trials<=1e6; p95_latency_ms real(S,)nonnegative; required bool(S,); at least one required slice. min_trials integer scalar1..1e6,min_success_rate real0..1,max_latency_ms real0..1e6. Return success_rate float64(S,) NaNwherezero trials; slice_pass bool(S,), failures list ofS lists ofreason strings in order insufficient_trials,safety_incident,low_success,latency; and release bool ALL required slices pass. slice_pass evaluates every slice, even optional ones; optional failures do not block release. Low_success applies ifftrials>0 and rate<minimum. Incident count>0 fails; equality at success/latency thresholds passes. Insufficient trial slices may have other reasons too. This is a synthetic deterministic evidence gate, NOT a physical safety guarantee or statistical confidence bound.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latency milliseconds; counts are evaluation trials/incidents, success rates dimensionless. Required slices are explicitly chosen scenario/embodiment conditions. Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time. Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.


## Example 1

trials=[10,10],successes=[9,10],incidents=[0,1],latency=[20,10],required=[True,True],min_trials10,min_success.9,max_latency20 returns slice_pass[True,False],failures=[[],["safety_incident"]],releaseFalse.

## Example 2

With required=[True,False] and the same evidence, releaseTrue but the optional failed slice remains visible in failures.
