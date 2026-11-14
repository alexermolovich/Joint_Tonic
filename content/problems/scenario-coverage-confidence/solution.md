# Solution explanation

Count trials and wins per declared bucket. Compute Wilson estimates only for observed buckets, retaining NaN for unknown rates and endpoints. Coverage counts observed buckets, not successes. Work O(N+B), storage O(B). Intervals are marginal and assume independent comparable trials.
