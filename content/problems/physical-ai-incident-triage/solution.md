# Solution approach

One validated pass and one windowed reduction, then sort C component summaries. O(E+C log C) time, O(C) reduction storage plus validation.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep unknown evidence distinct from a passing result. The cases exercise the worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
