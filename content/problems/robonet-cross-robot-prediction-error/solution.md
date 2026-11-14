# Solution explanation

Validate all evidence, group exact integer robot/episode IDs, and sum chunk residual/count pairs. Compute pooled and equal-episode means independently, retaining NaN for missing evidence. Work O(N+R log R), storage O(N+R).
