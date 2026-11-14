# Compare Slice Metrics Without Hiding Regressions

Implement compare_slice_regressions(slice_ids, baseline, candidate, slice_count, tolerance) -> dict.

slice_ids NumPy int64(N,), baseline/candidate float64(N,),0<=N<=100000, slice_count built-in non-bool int1..256. IDs in[0,S), losses finite0..1e6; tolerance built-in finite non-bool int/float0..1e6. Each row is a paired evaluation of the same robot episode under baseline and candidate using comparable dimensionless normalized loss; lower is better. Return counts:int64(S,), mean_delta:float64(S,), regressed:bool(S,), overall_delta:Python float or None, complete:bool. Per-row delta=candidate-baseline; mean_delta averages paired deltas within each slice, NaN for unobserved slices. regressed is true iff observed mean_delta>tolerance (strict; equality passes). overall_delta is the mean of ALL paired deltas, None when N=0. complete is true iff every declared slice is observed. Preserve inputs and return independent arrays; noncontiguous valid. Invalid contracts raise ValueError.

This exposes empirical slice regressions even when the pooled result improves. It does not perform significance tests, impute missing evidence, change weights to balance slices, or treat missing slices as passing proof. Caller must align episode identity before this function.

## Worked examples

### Pooled improvement hides a slice regression
ids[0,0,1], baseline[2,2,2], candidate[0,0,5], S2,tolerance0 returns counts[2,1], mean_delta[-2,3], regressed[False,True], overall_delta=-1/3, completeTrue.

### Missing slice and exact tolerance
ids[0], baseline[1], candidate[1.5], S2,tolerance0.5 returns counts[1,0], mean_delta[0.5,NaN], regressed[False,False], overall_delta0.5, completeFalse.

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
