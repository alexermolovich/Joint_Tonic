# Solution approach

Validate metadata and bounds; iterate sorted unique requirements, selecting the first rejection condition. O(R log R+E) time and O(R+E) validation/output memory.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep unknown evidence distinct from a passing result. The cases exercise the worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
