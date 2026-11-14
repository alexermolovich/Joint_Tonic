# Build a Continual-Learning Task Sequence

## Contract

continual_task_schedule(tasks, order, budget) -> list[dict]. tasks list of1..256 exact records{task_id,demo_ids,evaluation_seed_ids}; task IDs unique. Each ID list is a Python list of1..10000 unique built-in ints0..2^63-1; total demo IDs across tasks<=100000 and total seed IDs<=100000. Demo IDs must be globally unique across tasks to prevent duplicated demonstration allocation; seed IDs may repeat across tasks because they identify initial-state randomization, not trajectories. order is list containing each task ID exactly once. budget built-in int1..10000. For each task in order, select min(budget,len(demo_ids)) smallest demo IDs, preserve sorted unique evaluation seeds, and return exact{stage,task_id,selected_demo_ids,evaluation_seed_ids,cumulative_demo_count}, stage starts1. Count each task's selected demos once in cumulative_demo_count; no replay or future-task demos exposed. Selection is deterministic without RNG. This constructs a declared protocol, not an optimal task curriculum or LIBERO asset download.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

tasks a(demos[3,1],seeds[8]),b(demos[9],seeds[2,1]), order[b,a],budget1 -> rows(stage1,b,demos[9],seeds[1,2],cumulative1),(stage2,a,demos[1],seeds[8],cumulative2).

### Example 2

One task a(demos[5,2],seeds[0]),order[a],budget10 -> stage1,demos[2,5],seeds[0],cumulative2.

## Source and scope

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). It does not reproduce the full dataset loader, task suite or headline results.
