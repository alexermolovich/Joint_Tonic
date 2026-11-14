# Merge Online and Demonstration Replay

Replay sources may contain the same transition, especially after demonstrations are also copied into an online buffer. Preserve one immutable transition identity and report both sources instead of duplicating or overwriting evidence.

## Contract

```python
def merge_replay(online, demonstration):
    ...
```

online and demonstration are dicts with exactly keys ids, observations, actions, rewards, next_observations, terminated. ids integer(N,) globally unique transition IDs within each input,0<=ID<=1e6. observations/next_observations real(N, D), actions real(N, A), rewards real(N,), terminated bool(N,); 0<=N<=4096 per source,1<=D, A<=16 shared across both sources. All numeric features/actions/rewards already normalized, finite abs<=1e6. A transition ID repeated across sources must have exactly equal observation, executed action, reward, next observation, and termination after float64 conversion; reject any conflict. Return dict with same six fields plus origin int64(U,) bitmask1=online,2=demonstration,3=identical in both, sorted ascending unique global ID. Preserve every field and no input alias. Origin describes storage provenance, not proof that online actions were autonomous. No reset across a terminal transition is invented. This is original identity-preserving deterministic replay ingestion, not a sampling ratio or learner update.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Example 1

Use one-dimensional observations/actions. Online has ID `2`, observation `[0]`, action `[0.2]`, reward `1`, next observation `[1]`, terminated `False`. Demonstration has ID `1`, observation `[3]`, action `[0.1]`, reward `2`, next observation `[4]`, terminated `True`. Output IDs `[1, 2]`, observations `[[3], [0]]`, actions `[[0.1], [0.2]]`, rewards `[2, 1]`, next observations `[[4], [1]]`, terminated `[True, False]` and origin `[2, 1]`.

## Example 2

Place the same transition ID `5` in both sources: observation `[0]`, action `[0.2]`, reward `1`, next observation `[1]`, terminated `False`. The output contains exactly that one row with origin `[3]`. Changing either copy's action to `[0.3]` instead raises `ValueError`.
