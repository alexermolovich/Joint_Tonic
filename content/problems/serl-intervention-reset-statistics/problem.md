# Record Intervention and Reset Statistics

Training time, human effort and reset overhead describe different costs. Record them separately, and distinguish autonomous task outcomes from outcomes obtained with assistance.

## Contract

```python
def interaction_statistics(trial_duration, intervention_duration, reset_duration, task_success, reset_success, valid):
    ...
```

three durations real(N,)seconds[0,1e6], intervention_duration<=trial_duration; task_success/reset_success/valid bool(N,),0<=N<=16384. trial_duration excludes reset; intervention_duration is human-control time within trial. Return dict trials Python int valid count, autonomous_trials Python int count valid with intervention_duration==0; robot_time Python float sum(trial+reset)valid; human_time Python float sum intervention valid; reset_time Python float sum reset valid; human_fraction Python float human_time/sum trial or NaN when zero; task_success_rate/reset_success_rate Python float valid mean or NaN; autonomous_success_rate Python float success mean over valid zero-intervention trials or NaN. All masked durations still validated. Zero-duration autonomous trials permitted but their time fraction remains undefined if total trial time 0. Human assistance and resets are separate accounting categories; totals do not certify comparable initial-state distributions.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Example 1

Trial durations `[10, 20]`, human durations `[0, 5]`, reset durations `[2, 3]`, task success `[True, True]`, reset success `[True, False]`, all valid: trials `2`, autonomous_trials `1`, robot_time `35`, human_time `5`, reset_time `5`, human_fraction `1/6`, task_success_rate `1`, reset_success_rate `0.5` and autonomous_success_rate `1`.

## Example 2

For three empty duration arrays and three empty Boolean arrays, trials and autonomous_trials are `0`; robot_time, human_time and reset_time are `0.0`; human_fraction and all three success rates are `NaN`. No evidence is converted into a zero success rate.
