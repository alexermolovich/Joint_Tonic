# Solution approach

Validate bounded schema and workload, then inspect record/name union with ordered checks. O(total scalar entries+issue count log issue count) plus bounded feature lookups; no data coercion.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep missing evidence distinct from a passing result. The cases exercise worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
