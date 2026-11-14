# Solution explanation

Validate observed values only, then compute each supported difference using its exact stage indices. Compute forgetting only for a complete post-learning column segment and retain NaN elsewhere. Work O(K squared), output O(K) plus validated input copy.
