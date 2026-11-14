# Separate Task Semantics from Scene Variation

## Contract

semantic_scene_groups(records) -> list[dict]. records list of0..10000 exact records{task_id,verb,object_id,goal_id,scene_id}, all common identifiers, unique task_id. A semantic key is the ORDERED tuple(verb,object_id,goal_id); scene_id is excluded. Return exact records{semantic_key,task_ids,scene_ids,has_scene_variation}, sorted lexically by semantic_key, with task_ids sorted and scene_ids sorted UNIQUE. has_scene_variation is True iff at least2 distinct scenes occur in that semantic group. Repeated scene IDs across different semantic groups do not merge them; two task IDs with same semantics and scene are valid distinct tasks. No language parsing or geometry is inferred. This indexes provided factor annotations rather than reproducing LIBERO task taxonomy.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

tasks a(pick,cup,tray,kitchen),b(pick,cup,tray,lab),c(place,cup,tray,kitchen) -> group(pick,cup,tray):tasks[a,b],scenes[kitchen,lab],True; group(place,cup,tray):tasks[c],scenes[kitchen],False.

### Example 2

Two tasks a,b both(pick,cup,tray,kitchen) -> one group,task_ids[a,b],scene_ids[kitchen],has_scene_variationFalse.

## Source and scope

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). It does not reproduce the full dataset loader, task suite or headline results.
