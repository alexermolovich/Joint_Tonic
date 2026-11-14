# Aggregate Seeded Benchmark Returns

## Goal

A training seed with many recorded evaluation episodes should not silently receive more weight than another seed.

## Contract

seeded_return_summary(task_ids, seed_ids, returns) -> dict{task_ids,seeds,counts,means,task_means,overall}. task_ids and seed_ids int64(E,), values0..2^63-1; returns float(E,),0<=E<=100000, finite abs<=1e6. Multiple episodes per(task,seed) are valid. Return sorted unique task_ids int64(M,), seeds int64(S,), counts int64(M,S), means float64(M,S) with NaN at missing cells. task_means float64(M,) averages PRESENT seed means equally (not all episodes); overall Python float averages task_means equally. Empty input yields empty arrays including(0,0) and overallNaN. Require M*S<=1e6. All returns use the same supplied reward/horizon convention. This exposes unequal evaluation episode counts rather than letting prolific seeds dominate; it does not estimate variance or replace IQM.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

task_ids=[0,0,0,1],seed_ids=[1,1,2,1],returns=[0,2,9,4] -> tasks[0,1],seeds[1,2],counts[[2,1],[1,0]],means[[1,9],[4,NaN]],task_means[5,4],overall4.5.

### Example 2

task_ids=[2,2],seed_ids=[7,7],returns=[-1,1] -> counts[[2]],means[[0]],task_means[0],overall0.

## Source and scope

Original bounded component associated with [2018-deepmind-control-suite](https://arxiv.org/abs/1801.00690). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
