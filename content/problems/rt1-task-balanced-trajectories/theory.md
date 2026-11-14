# Sample a Task-Balanced Trajectory Batch

## Intuition

A common task can dominate training when sampling trajectories uniformly. Pick a task uniformly first, then pick a demonstration inside that task so rare tasks receive equal task-level probability.

## Mathematical mechanism

For G observed tasks and n_g trajectories in task g, each trajectory i in g has probability 

$$p(i)=1/(G n_g)$$

. Supplied fractions $u,v\in[0,1)$ select $g=\lfloor Gu\rfloor$ in sorted task order and local index $j=\lfloor n_gv\rfloor$. M is dataset size and N is requested batch size; both index arrays are dimensionless.

## Visual computation trace

| Stage | Example |
|---|---|
| Task IDs | [2,2,5] |
| Sorted groups | 2:[0,1], 5:[2] |
| Fractions | [0.2,0.8] |
| Chosen task/local index | 2 / 1 |
| Dataset index | 1 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

For task_ids=[2,2,5] and uniforms=[[0.2,0.8],[0.8,0.2]], return [1,2]. The first draw selects the second trajectory in task2; the second selects the only task5 trajectory.

## Why this matters on a robot

Task balance differs from frame balance: a long demonstration may still contribute more tokens later. Reordering files changes these indices, so record dataset ordering and supplied fractions with the experiment. Sampling with replacement allows repeated indices and does not promise an exactly balanced finite batch.

## Physical contract and limits

IDs and sampling fractions are dimensionless; trajectory indices preserve the caller dataset ordering. One row is one independent draw with replacement, not a control timestep. Original task-balanced sampler motivated by multi-task RT-1 data; the exact two-stage inverse-CDF contract is a teaching choice, not a reproduction of its dataset distribution.

Source: [primary paper](https://arxiv.org/abs/2212.06817). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
