# Solution approach

Validate policy settings, then exclude warmup and invalid records. Check all included records and group them by hardware. Sort hardware keys so output is deterministic.

For each group, compute mean correctness, linear latency quantiles, sequential throughput and maximum memory. Compute mean accuracy per slice. Append all failed global rules in the documented fixed order, followed by missing/regressed baseline slice rules in sorted slice order.

An empty measured collection returns a specific no_samples failure. Numeric threshold equality passes; a tiny tolerance is applied only to slice-drop comparison as documented.

Sorting latency samples costs O(N log N) overall. Grouping and quality/memory aggregation are linear. The simple reference constructs slice subsets explicitly; a one-pass slice accumulator is an equivalent optimization.
