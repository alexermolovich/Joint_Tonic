# Bootstrap a Stratified Performance Profile

## Goal

A performance profile asks what fraction of runs clear each score threshold.

## Contract

stratified_profile(scores, thresholds, resample_indices) -> dict{profile,replicates}. scores float(M,N),1<=M,N<=256. thresholds float(Q,),0<=Q<=128, arbitrary order/duplicates retained. resample_indices int64(B,M,N),0<=B<=512, each index in[0,N), at most1e6 indices and B*M*N*max(Q,1)<=2e7. Bootstrap replicate b independently gathers N supplied indices within each TASK row; task rows themselves are fixed, never pooled or resampled. Return profile float64(Q,) = mean(scores>threshold), replicates float64(B,Q) from gathered scores. Strict >, not >=. Supplied resampling indices make the exercise replayable without RNG; this computes empirical replicate curves, not percentile intervals or coverage guarantees. O((B+1)*M*N*Q), avoid allocating B*M*N*Q at once.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

scores=[[0,2],[10,12]], thresholds=[2,10], indices=[[[1,1],[0,0]]] -> profile=[0.5,0.25], replicates=[[0.5,0]].

### Example 2

scores=[[1]], thresholds=[1,0,1], indices shape(0,1,1) -> profile=[0,1,0], replicates shape(0,3).

## Source and scope

Original bounded component associated with [2021-rliable-statistical-precipice](https://arxiv.org/abs/2108.13264). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
