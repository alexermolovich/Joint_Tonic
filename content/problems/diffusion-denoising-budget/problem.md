# Budget Denoising Steps Against Control Frequency

More denoising iterations can improve a sampler while missing a robot deadline. Separate a measured cost model from the policy-quality question and choose only among candidates that fit the control period.

## Contract

`denoising_budget(candidate_steps,step_ms,overhead_ms,frequency_hz)` takes integer candidate_steps(K,),1<=K<=128, each1..10000; positive step_ms<=1e6, overhead_ms in [0,1e6], frequency_hz in [0.001,10000]. Return dict latency_ms:float64(K,) = overhead+steps*step_ms, feasible:bool(K,) for latency<=1000/frequency, and selected_steps:Python int equal largest feasible count, or0 if none. Preserve candidate order in arrays; duplicate counts permitted. This conservative contract requires a new plan every single control period.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latency milliseconds; control frequency Hertz; counts dimensionless. One planning invocation per period1000/frequency_hz ms; overlap or amortization across action windows is outside this task. Original serving-budget exercise inspired by Diffusion Policy inference scheduling. A constant measured per-step cost is an explicit approximation, not a published timing guarantee.


## Example 1

candidate_steps=[1,4,5], step_ms=2, overhead_ms=1, frequency_hz=100 returns latency_ms=[3,9,11], feasible=[True,True,False], selected_steps=4.

## Example 2

candidate_steps=[2,1], step_ms=5, overhead_ms=0, frequency_hz=100 returns [10,5], both feasible, selected_steps=2. Equality is allowed and candidate order is not sorted.
