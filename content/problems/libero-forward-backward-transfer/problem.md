# Compute a Forward and Backward Transfer Matrix

## Contract

continual_transfer_report(rates, observed) -> dict{forward,backward,forgetting,forward_mean,backward_mean,forgetting_mean,final_mean}. rates float(K+1,K),1<=K<=256; observed bool same shape. Observed rates must finite[0,1]; unobserved entries may contain arbitrary finite/NaN/Inf placeholders and are ignored. Rows stage0(initial) throughK(final), columns task j=0..K-1 learned at stage j+1. forward[j]=rates[j,j]-rates[0,j] only j>=1 and both observed; backward[j]=rates[K,j]-rates[j+1,j] only j<K-1 and both observed; otherwise NaN. forgetting[j]=max(rates[j+1:K+1,j])-rates[K,j] only j<K-1 and ALL those post-learning stages observed; otherwise NaN. Including final stage makes forgetting nonnegative. Return three float64(K,) vectors; means average only finite entries, NaN if none. final_mean averages observed final-row tasks or NaN if none. This explicit bounded protocol distinguishes transfer from completeness; it is not asserted to match every published LIBERO metric variant.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

rates=[[.1,.2],[.8,.4],[.6,.9]], observed allTrue -> forward[NaN,.2],backward[-.2,NaN],forgetting[.2,NaN],forward_mean.2,backward_mean-.2,forgetting_mean.2,final_mean.75.

### Example 2

K1,rates[[0],[1]],observed allTrue -> allthree vectors[NaN],allthree transfer meansNaN,final_mean1.

## Source and scope

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). It does not reproduce the full dataset loader, task suite or headline results.
