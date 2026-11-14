# Sample a Task-Balanced Trajectory Batch

A common task can dominate training when sampling trajectories uniformly. Pick a task uniformly first, then pick a demonstration inside that task so rare tasks receive equal task-level probability.

## Contract

`sample_task_balanced(task_ids, uniforms)` receives integer task_ids(M,), 1<=M<=10000, nonnegative IDs<=1e6, and real uniforms(N,2), 0<=N<=10000, with entries in [0,1). Sort unique task IDs increasingly. For each row (u,v), choose sorted task index floor(u*G), then choose floor(v*count) within that task’s original trajectory indices. Return int64 indices(N,). Empty uniforms shape(0,2) returns empty; task_ids cannot be empty. No RNG call is made.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

IDs and sampling fractions are dimensionless; trajectory indices preserve the caller dataset ordering. One row is one independent draw with replacement, not a control timestep. Original task-balanced sampler motivated by multi-task RT-1 data; the exact two-stage inverse-CDF contract is a teaching choice, not a reproduction of its dataset distribution.


## Example 1

For task_ids=[2,2,5] and uniforms=[[0.2,0.8],[0.8,0.2]], return [1,2]. The first draw selects the second trajectory in task2; the second selects the only task5 trajectory.

## Example 2

For task_ids=[7,7] and uniforms=[[0,0],[0.99,0.99]], return [0,1]. Only within-task choice changes.
