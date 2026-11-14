# Compute Per-Embodiment and Transfer Metrics

A single average hides whether a shared policy succeeds only on the embodiment it was trained for. Preserve the training-to-evaluation direction and keep untested combinations visibly unknown.

## Contract

`embodiment_transfer_metrics(train_ids,test_ids,success,num_embodiments)` takes integer train_ids(N,),test_ids(N,), bool success(N,),0<=N<=10000, integer E=num_embodiments1..64, IDs0..E-1. Return dict count:int64(E,E), success_rate:float64(E,E), same_embodiment_rate:float or None, transfer_rate:float or None. Matrix rows are training embodiment IDs, columns evaluation embodiment IDs. Rates at empty cells are NaN. Same/transfer aggregate success across individual diagonal/off-diagonal attempts (micro averages), not an unweighted mean of cell rates. No observations in an aggregate gives None.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Rates dimensionless; IDs reference a versioned embodiment registry. Each row is one episode evaluation, not an action timestep; train/test IDs label model-training and deployment embodiment. Original cross-embodiment evaluation aggregation inspired by OXE. A matrix cell measures supplied outcomes and cannot prove transfer causality without controlled baselines.


## Example 1

train_ids=[0,0,0], test_ids=[0,1,1], success=[True,True,False], E=2 returns count=[[1,2],[0,0]], rates=[[1,0.5],[NaN,NaN]], same_embodiment_rate=1 and transfer_rate=0.5.

## Example 2

train_ids=[1], test_ids=[1], success=[False], E=2 yields same_embodiment_rate=0 and transfer_rate=None; only cell(1,1) has count1/rate0.
