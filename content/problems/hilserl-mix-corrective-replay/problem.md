# Mix Intervention and Autonomous Replay

Corrective and autonomous transitions answer different questions. Use explicit quotas and recorded priorities to build a reproducible batch while preserving the commands that were executed.

## Contract

```python
def mix_corrective_replay(executed_actions, intervention, priorities, batch_size, intervention_fraction):
    ...
```

executed_actions real(N, A)normalized[-1,1], intervention bool(N,), priorities real(N,)in[0,1),0<=N<=16384,1<=A<=16; batch_size built-in int 0..4096; intervention_fraction scalar[0,1]. Human quota=floor(batch_size*fraction+.5) (half up), autonomous quota=batch-human. Require enough distinct records in each pool; no silent quota adjustment. Within each pool choose quota lowest supplied priorities, tie lowest original index, without replacement. Output selected human rows first then autonomous rows, each in priority/index order. Return dict indices int64(B,), actions float64(B, A), intervention bool(B,), counts int64(2,)ordered[human, autonomous]. Priorities may be recorded random draws but no RNG inside function. Supplied actions are executed actions, not overwritten policy proposals. This original source-exclusive sampling recipe is not claimed to exactly match HIL-SERL's potentially overlapping online/demonstration buffer layout.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Example 1

Actions `[[0.1], [0.2], [0.3], [0.4]]`, intervention `[True, False, True, False]`, priorities `[0.8, 0.4, 0.1, 0.2]`, batch size `2` and fraction `0.5` produce indices `[2, 3]`, actions `[[0.3], [0.4]]`, intervention `[True, False]` and counts `[1, 1]`.

## Example 2

With the same records, batch size `1` and fraction `0.5`, half-up rounding requests one human row. Return indices `[2]`, actions `[[0.3]]`, intervention `[True]` and counts `[1, 0]`. If no human row exists, raise `ValueError`.
