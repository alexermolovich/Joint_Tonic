# Estimate Scenario Coverage and Confidence Intervals

Implement scenario_coverage(bucket_ids, success, bucket_count) -> dict.

bucket_ids is NumPy int64(N,), success bool(N,), N in0..100000. bucket_count is a built-in non-bool int1..256; IDs in[0,B). Each row is one independent evaluation scenario with a Boolean task-success outcome. Return counts:int64(B,), success_rate:float64(B,), wilson:float64(B,2), coverage:Python float. Coverage is number of observed buckets divided by B. For each observed bucket use the arithmetic success fraction and the Wilson interval below with fixed z=1.96; clip its two endpoints to[0,1]. Unobserved rates and both interval endpoints are NaN. Preserve inputs and return independent storage. Noncontiguous arrays are valid. Invalid types/dtypes/shapes/ranges raise ValueError.

For n trials and k successes, p=k/n, d=1+z²/n, c=(p+z²/(2n))/d, h=z*sqrt(p*(1-p)/n+z²/(4n²))/d; interval[max(0,c-h),min(1,c+h)]. Rates and intervals are dimensionless. This nominal 95% marginal binomial interval assumes independent, comparable Bernoulli trials within each bucket. It is not a simultaneous guarantee, transfer proof, or interval for unseen buckets.

## Worked examples

### One success and one unknown bucket
ids=[0] int64, success=[True] bool, B=2 returns counts[1,0], rate[1,NaN], wilson approximately[[0.2065432915,1],[NaN,NaN]], coverage0.5.

### One success in two trials
ids=[0,0], success=[True,False], B=1 returns counts[2], rate[0.5], wilson approximately[[0.0945286548,0.9054713452]], coverage1.

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
