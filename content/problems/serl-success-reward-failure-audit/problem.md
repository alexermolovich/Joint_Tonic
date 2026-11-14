# Validate Success-Classifier Rewards on Robot Failures

A success classifier can be exploited if it mistakes recurring robot failures for completed tasks. Inspect false rewards by failure category instead of trusting only aggregate accuracy.

## Contract

```python
def audit_success_rewards(probabilities, success, failure_type, valid, threshold, num_failure_types):
    ...
```

probabilities real(N,) in[0,1], success/valid bool(N,), failure_type int(N,),0<=N<=16384. num_failure_types built-in int 1..32; true successes require failure_type=-1 and failures require integer0..K-1, including masked records. threshold scalar[0,1], predicted success when probability>=threshold. Return dict confusion int64(4,) ordered[TP, FP, FN, TN] over valid observations; precision Python float TP/(TP+FP) or NaN no positive predictions; recall Python float TP/(TP+FN) or NaN when no actual positive labels (TP+FN=0); failure_counts int64(K,) valid true failure counts by type; false_positive_counts int64(K,); false_positive_rate float64(K,) FP/count or NaN absent type. True-success examples never enter failure-type counts. Original operational audit of a supplied classifier, not training the reward model or certifying behavior.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Example 1

For probabilities `[0.9, 0.8, 0.2]`, success labels `[True, False, False]`, failure types `[-1, 0, 1]`, all valid, threshold `0.5` and two failure types, return confusion `[1, 1, 0, 1]`, precision `0.5`, recall `1.0`, failure counts `[1, 1]`, false-positive counts `[1, 0]` and rates `[1.0, 0.0]`.

## Example 2

One failure of type 0 has probability `0.5`. With threshold `0.5` and two failure types, it is a false positive: confusion `[0, 1, 0, 0]`, precision `0`, recall `NaN`, failure counts `[1, 0]`, false-positive counts `[1, 0]` and rates `[1, NaN]`.
