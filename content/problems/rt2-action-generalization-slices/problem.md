# Monitor Invalid Actions and Semantic Generalization Slices

An overall success percentage can hide a policy that emits malformed commands on unfamiliar instructions. Report validity and task success on the same denominator for every declared evaluation slice.

## Contract

`action_slice_metrics(valid,success,slice_ids,num_slices)` receives bool(N,) valid and success, integer(N,) slice_ids,0<=N<=10000; integer num_slices1..128, IDs in[0,num_slices). Return dict count:int64(S,), invalid_rate:float64(S,), success_rate:float64(S,). Count all attempted actions. Invalid rate counts ~valid/count. Success counts valid & success/count, so invalid commands cannot count as successes even if a source flag says success. Unobserved slices have count0 and both rates NaN. Each attempt has one already assigned semantic slice.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Rates are dimensionless attempt fractions; semantic slice IDs preserve external evaluation labels. Each row is one evaluated attempt, not a timestep; attempts may come from different episodes. Original monitoring component inspired by RT-2 semantic-generalization evaluation. It computes supplied slice metrics and does not infer semantic novelty from images or claim paper-level success.


## Example 1

valid=[True,False], success=[True,True], slice_ids=[0,0], num_slices=2 returns count=[2,0], invalid_rate=[0.5,NaN], success_rate=[0.5,NaN]. The invalid row is not a success.

## Example 2

valid=[True,True], success=[False,True], slice_ids=[1,0], num_slices=2 returns count=[1,1], invalid_rate=[0,0], success_rate=[1,0]. Output order is slice-ID order.
