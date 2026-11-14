# Gate an Online Policy Update

A candidate that succeeds only with human corrections has not shown autonomous improvement. Remove assisted trials from both policies before comparing the observed evaluation rates.

## Contract

```python
def gate_policy_update(success, safety_violation, assisted, valid, current_version, candidate_version, min_autonomous_trials, allowed_success_drop, max_violation_rate):
    ...
```

success, safety_violation, assisted, valid bool(2, N),0<=N<=4096; row 0 current, row 1 candidate on a declared fixed evaluation protocol, no paired-seed assumption. current_version/candidate_version built-in int 0..1e9, min_autonomous_trials int 1..4096, allowed_success_drop/max_violation_rate scalar[0,1]. Eligible evidence=valid AND NOT assisted. Compute each row count, success rate, violation rate (NaN absent). Return dict counts int64(2,), success_rate/violation_rate float64(2,), checks bool(4,)ordered[newer_version, both_have_min_trials, candidate_success>=current_success-allowed_drop, candidate_violation<=limit], accepted Python bool all checks. Missing rates make comparisons False. Successful assisted trials cannot improve autonomous evidence. Observed-rate gate only; no uncertainty guarantee, hardware execution authorization or automatic deployment.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Example 1

Both policies have two valid autonomous trials. Success is `[[True, False], [True, True]]`, with no violations or assistance. Versions `1` and `2`, minimum trials `2`, allowed drop `0` and maximum violation rate `0` produce counts `[2, 2]`, success_rate `[0.5, 1]`, violation_rate `[0, 0]`, checks `[True, True, True, True]` and accepted `True`.

## Example 2

Mark both candidate trials in Example 1 as assisted. Return counts `[2, 0]`, success_rate `[0.5, NaN]`, violation_rate `[0, NaN]`, checks `[True, False, False, False]` and accepted `False`.
