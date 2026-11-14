# Label Human Intervention Segments

A human override changes the action that the robot actually experiences. Replay must record that executed command and identify each contiguous intervention without blending across episode resets.

## Contract

```python
def label_interventions(policy_actions, human_actions, intervention, episode_ids):
    ...
```

policy_actions/human_actions real(N, A), intervention bool(N,), episode_ids int(N,)nonnegative nondecreasing<=1e6; 0<=N<=16384,1<=A<=16, actions normalized[-1,1]. Both proposed and human commands validated even when not selected. Return dict executed_actions float64(N, A) chosen human when intervention else policy; segment_id int64(N,) -1 on autonomous rows, consecutive 0-based ID for each maximal contiguous human run inside one episode; segments int64(K,3) rows[episode ID, start index, end index exclusive] ordered by start. Consecutive human rows across episode boundary are separate segments. Recorded action sources do not set terminal flags; this task does not infer task completion. All commands share the caller-declared controller frame/control interval; no position-to-velocity conversion.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Example 1

Policy actions `[[0.1], [0.2], [0.3]]`, human actions `[[0.9], [0.8], [0.7]]`, intervention `[False, True, True]` and episodes `[0, 0, 0]` produce executed_actions `[[0.1], [0.8], [0.7]]`, segment_id `[-1, 0, 0]` and segments `[[0, 1, 3]]`.

## Example 2

Policy actions `[[0], [0]]`, human actions `[[0.4], [0.5]]`, intervention `[True, True]` and episodes `[0, 1]` produce executed_actions `[[0.4], [0.5]]`, segment_id `[0, 1]` and segments `[[0, 0, 1], [1, 1, 2]]`. The episode boundary splits the human run.
