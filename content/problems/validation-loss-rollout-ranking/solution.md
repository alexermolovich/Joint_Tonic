# Solution approach

Validate records, sort once by(loss,ID) and once by exact descending success fraction thenID; return the two ID lists and winner disagreement. Use exact rational arithmetic or integer comparison, O(NlogN).

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
