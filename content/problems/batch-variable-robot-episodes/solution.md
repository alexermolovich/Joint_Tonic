# Solution approach

Validate bounded float64 arrays and shared width; allocate batch, mask and lengths; copy prefixes. Time O(BLD), memory O(BLD), with padded allocation explicitly bounded.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
