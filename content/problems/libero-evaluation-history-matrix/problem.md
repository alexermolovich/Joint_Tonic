# Record a Continual-Learning Evaluation Matrix

## Contract

continual_evaluation_matrix(task_order, events) -> dict{counts,successes,rates}. task_order list1..256 unique common taskIDs. events list0..100000 exact records{evaluation_id,stage,task_id,success}; evaluation_id commonID; stage built-in int0..K where K=len(task_order), task_id must be declared, success bool. stage0 is initial policy; stage i is after learning first i tasks. A repeated identical evaluation_id record is idempotent; any conflicting field for same evaluation_id raises ValueError. Distinct IDs remain distinct trials even if other fields coincide. Return counts/successes int64(K+1,K), rates float64(K+1,K)=successes/counts with NaN at zero count. Column order is task_order; rows are learning stages including0. Observing future tasks at earlier stages is valid for forward-transfer evidence. No missing cell is imputed.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

task_order=[a,b],events e1(stage0,b,False),e2(stage1,a,True),e2 repeated -> counts[[0,1],[1,0],[0,0]],successes[[0,0],[1,0],[0,0]],rates[[NaN,0],[1,NaN],[NaN,NaN]].

### Example 2

task_order=[a], events e1(stage1,a,True),e2(stage1,a,False) -> counts[[0],[2]],successes[[0],[1]],rates[[NaN],[0.5]].

## Source and scope

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). It does not reproduce the full dataset loader, task suite or headline results.
