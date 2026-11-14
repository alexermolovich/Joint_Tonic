---
{
  "schema_version": 1,
  "problem_id": "ray-immutable-object-locations",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Track Immutable Artifact References",
  "summary": "Track Immutable Artifact References",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "operational-evidence",
    "2017-ray"
  ],
  "paper_ids": [
    "2017-ray"
  ],
  "paper_sections": [
    "Operational component discussed in Theory; explicit original teaching policy"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; local bubblewrap baseline",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.track_artifact_locations",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "size_bytes/physical_bytes": "bytes",
      "nodes": "replica location identities"
    },
    "axes": "Ordered event stream; output one immutable artifact row with a sorted node set.",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "Ordered event stream; output one immutable artifact row with a sorted node set."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-09,
    "atol": 1e-10,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-oracle",
      "edge-shapes",
      "invalid-contract",
      "preservation",
      "scale"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "8137ba6576b182cb6ee31786f3048f7ca9d2b4037c662187102c86fb4e8ca112"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-394",
    "primary_urls": [
      "https://arxiv.org/abs/1712.05889"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2017-ray.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "research_curator",
    "perception_completion"
  ]
}
---

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
