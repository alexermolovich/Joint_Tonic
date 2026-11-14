# Solution approach

Validate names and scalar bounds; memoize exact SHA-256 bucket decisions by scene; append episodes in original order. Complexity O(N+S) for N episodes and S unique scenes, with bounded ID lengths.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
