# Schedule Actor-Learner Updates

The learner should not consume an unbounded update budget merely because it runs faster than robot collection. Track owed updates exactly, cap work per scheduling tick, and carry the remainder forward.

## Contract

```python
def schedule_learner(new_transitions, warmup, ratio_numerator, ratio_denominator, max_updates_per_tick, publish_every):
    ...
```

new_transitions integer(T,) in[0,10000],0<=T<=4096; warmup built-in int[0,1e6], ratio_numerator/denominator built-in ints1..32, max_updates_per_tick int 1..1000, publish_every int 1..1000. All counters start at 0. At tick t cumulative data D=sum of new transitions; target updates=floor(max(D-warmup,0)*numerator/denominator) using exact integer arithmetic. Emit min(max_updates_per_tick, target updates-completed updates); backlog carries across ticks including ticks with no new data. Each optimizer update increments model version by1. Publish the latest completed version when floor(completed/publish_every) increases since previous tick, else keep prior published version. Return dict updates int64(T,), completed int64(T,), backlog int64(T,), published_version int64(T,), publish bool(T,). A crossing can skip versions; publish current latest once rather than inventing many network messages. Original synchronous accounting model of an asynchronous actor/learner schedule; no wall-clock or hardware throughput guarantee.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Example 1

With new transitions `[2, 0, 1]`, warmup `0`, ratio `2/1`, cap `3` and publication interval `2`, return updates `[3, 1, 2]`, completed `[3, 4, 6]`, backlog `[1, 0, 0]`, published_version `[3, 4, 6]` and publish `[True, True, True]`.

## Example 2

With new transitions `[2, 1]`, warmup `2`, ratio `1/2`, cap `10` and publication interval `2`, the floored targets are `[0, 0]`. All four integer outputs are `[0, 0]`, and publish is `[False, False]`.
