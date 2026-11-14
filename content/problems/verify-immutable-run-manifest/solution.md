# Solution approach

Validate bounded mappings and payload lengths, use hashlib.sha256 for common artifacts, report set differences and mismatched values. O(total bytes+N log N) time with bounded O(N) metadata/output; no payload copies or external access.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep unknown evidence distinct from a passing result. The cases exercise the worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
