# Solution approach

Validate rows and accumulate integer counts by slice; sort slices and aggregate pooled counts and equal-task rates per quality. O(N+SlogS) time and O(S) memory for S<=10000 slices.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
