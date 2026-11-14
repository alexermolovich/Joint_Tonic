# Solution explanation

Validate each column is a complete permutation, independently of other columns. Add the within-stratum jitter and divide by N. This fills each marginal interval once; correlated columns remain valid because joint coverage is not required. Sorting validation O(N log N), output/storage O(N).
