# Solution approach

Validate names/counts/totals, align the union, compute per-histogram frequencies and signed deltas, then the maximum distance. O(C log C) time and O(C) output space.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
