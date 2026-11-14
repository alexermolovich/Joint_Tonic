# Solution approach

Validate each occurrence and accumulate channel minima/maxima plus presence counts without concatenating episodes. O(total input scalars) arithmetic and O(sum of signal widths) accumulator memory. Return fresh float64 range arrays.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
