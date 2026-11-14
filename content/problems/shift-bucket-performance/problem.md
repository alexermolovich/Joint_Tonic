# Measure Performance Across Shift Buckets

Implement shift_bucket_metrics(bucket_ids, errors, bucket_count) -> dict.

bucket_ids is NumPy int64(N,), errors matching float64(N,),0<=N<=100000. bucket_count is a built-in non-bool int1..256. IDs are in[0,bucket_count), errors finite in[0,1000000]. Each supplied error is a comparable dimensionless normalized per-scenario loss; lower is better. Noncontiguous inputs are valid. Return new arrays counts:int64(B,), mean_error:float64(B,), worst_error:float64(B,), B=bucket_count, in increasing bucket-ID order. Unobserved buckets have count0 and both floating metrics NaN. Observed buckets use arithmetic mean and maximum. Preserve inputs; outputs do not alias inputs or each other. Invalid contracts raise ValueError.

Bucket identity is supplied, not inferred from images. This groups equal-weight scenario measurements; it does not mix raw metres/radians, estimate confidence, or claim a pooled score proves transfer.

## Worked examples

### A weak and an unmeasured slice
For ids[0,1,0], errors[1.,9.,3.], bucket_count3, return counts[2,1,0], mean_error[2.,9.,NaN], worst_error[3.,9.,NaN].

### Empty evidence
With empty int64 IDs, empty float64 errors and bucket_count2, return counts[0,0] and both metric arrays[NaN,NaN].

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
