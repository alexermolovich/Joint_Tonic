# Solution: preserve intervals, then select observed ranks

Validate the paired lists and timestamp values. Subtract completion minus arrival using Python integers before converting anything to floating point. This preserves short intervals even when the clock origin is near the int64 maximum.

Sort the durations once. For integer percentage r, the one-based rank is (r*N+99)//100. Subtract one for list indexing and convert the selected duration from nanoseconds to milliseconds. Empty traces return explicit None values rather than inventing a zero measurement.

This nearest-rank convention chooses the lower middle observation for an even-count p50; an interpolating percentile API may return a different result. Time is O(N log N), memory O(N). Preserve workload and timing-boundary metadata elsewhere; these numbers alone do not certify a benchmark.
