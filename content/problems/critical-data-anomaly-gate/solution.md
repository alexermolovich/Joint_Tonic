# Solution approach

Validate lists and tuple fields, build source sets and a severity map, derive sorted critical/warning/missing outputs. O(A+S+(A+S)log(A+S)) time including sorting; bounded metadata storage.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
