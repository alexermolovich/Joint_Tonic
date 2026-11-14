## Example 1

candidate_steps=[1,4,5], step_ms=2, overhead_ms=1, frequency_hz=100 returns latency_ms=[3,9,11], feasible=[True,True,False], selected_steps=4.

## Example 2

candidate_steps=[2,1], step_ms=5, overhead_ms=0, frequency_hz=100 returns [10,5], both feasible, selected_steps=2. Equality is allowed and candidate order is not sorted.
