# Track Immutable Artifact References

## Contract

`track_artifact_locations(events) -> dict`. events is a Python list of 0..50000 ordered records. A put has exactly {op:"put", artifact_id, node_id, sha256, size_bytes}; size_bytes is int in 0..10^12. An evict has exactly {op:"evict", artifact_id, node_id}. At most 10,000 distinct artifacts and10000 distinct nodes may occur. First put declares artifact immutable identity(sha256, size_bytes). Every later put for that artifact must agree, even after all replicas were evicted; otherwise raise ValueError. Evict requires a previously declared artifact; eviction of an absent replica is an idempotent no-op. A repeated put on the same node is an idempotent no-op. Event order is meaningful.

Return {artifacts:[{artifact_id, sha256, size_bytes, nodes, lost}], physical_bytes}. Rows and each unique node list are lexically sorted. lost is True iff nodes is empty. physical_bytes is a Python int sum(size_bytes*replica_count). Different artifact IDs remain distinct even if hashes match. No content bytes are hashed and no byte-level deduplication is assumed. Work O(E) plus output sorting.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

put object a(hash"1"*64, size=4) on n1, repeat same put, then put on n2 produces nodes["n1","n2"], lost=False, physical_bytes=8.

put a(size=4) on n1, evict a/n1 twice produces nodes[], lost=True, physical_bytes=0, while retaining a's immutable hash and size. A later put with a different hash is invalid.

## Source and scope

Original bounded component inspired by [2017-ray](https://arxiv.org/abs/1712.05889). It does not reproduce the full paper or establish hardware safety or data-use authorization.
