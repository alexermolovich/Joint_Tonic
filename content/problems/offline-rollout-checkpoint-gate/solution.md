# Solution approach

Validate bounded candidate evidence; filter all three gates; select by exact success fraction, loss and ID. Sorting O(NlogN) is acceptable; a single-pass exact comparator also works.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
