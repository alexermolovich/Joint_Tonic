# Solution approach

Validate exact episode fields and channel descriptors; construct a source lookup and compatible unit scales; copy/reorder converted columns with independent output arrays and metadata. O(TD+S), bounded by T<=10000,D<=64.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
