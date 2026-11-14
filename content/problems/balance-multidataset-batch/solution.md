# Solution approach

Validate integer weights and batch size; compute exact floor quotas; allocate R extras by sorted remainder/ID; emit sorted counts. O(KlogK) time and O(K) space.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
