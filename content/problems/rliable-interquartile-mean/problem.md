# Compute an Interquartile Mean Benchmark Score

## Goal

A few exceptionally lucky or unlucky training seeds can dominate an ordinary mean.

## Contract

interquartile_score(scores) -> float. scores is float32/64(M,N), 1<=M,N<=2048, M*N<=1000000, dimensionless already-normalized scores with task rows and independent training-seed columns. Pool all scores, sort, remove floor(M*N/4) from EACH end, average remaining. This pins the finite-sample convention used by rliable's 25%-trimmed mean; it does not fractionally trim boundaries or trim each task separately. All tasks have the same run count. Work O(K log K), storage O(K), K=M*N.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

[[0,1,2,3],[4,5,6,100]] -> 3.5; sorted middle is [2,3,4,5].

### Example 2

[[1,2,100]] -> 103/3; floor(3/4)=0 so all three scores remain.

## Source and scope

Original bounded component associated with [2021-rliable-statistical-precipice](https://github.com/google-research/rliable/blob/master/rliable/metrics.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
