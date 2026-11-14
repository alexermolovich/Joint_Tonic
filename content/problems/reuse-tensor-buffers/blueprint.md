---
{
  "schema_version": 1,
  "problem_id": "reuse-tensor-buffers",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Reuse Tensor Buffers with Liveness Analysis",
  "summary": "Reuse Tensor Buffers with Liveness Analysis",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2018-tvm"
  ],
  "paper_ids": [
    "2018-tvm"
  ],
  "paper_sections": [
    "Mechanism described in theory; bounded teaching contract"
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
  "entrypoint": "solution.reuse_tensor_buffers",
  "physical_contract": {
    "frames": [
      "No spatial transform; named records retain their supplied identity"
    ],
    "units": {
      "size": "bytes",
      "capacity": "bytes",
      "start/end": "dimensionless logical execution steps"
    },
    "axes": "Each record is one contiguous storage request; lifetime [start,end).",
    "timestamp_assumptions": "No wall-clock timestamps; deterministic logical inputs only.",
    "batching": "Each record is one contiguous storage request; lifetime [start,end)."
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
    "evaluator_sha256": "4c5e6963e1d81f350308e137e712a59b9ac775fbb85baf8f85f3c990d1e8a554",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2018-tvm](https://www.usenix.org/conference/osdi18/presentation/chen). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://www.usenix.org/conference/osdi18/presentation/chen"
    ],
    "paper_card": "research/papers/mlops-sim2real/2018-tvm.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Reuse Tensor Buffers with Liveness Analysis

Implement reuse_tensor_buffers(tensors) -> dict.

tensors is a list of 0–10000 tuples(name,size_bytes,start,end). Names are unique ASCII IDs matching[a-z][a-z0-9_-]{0,63}. Size is built-in non-bool int in[1,10**9]; start/end are built-in ints in[0,10**9] with start<end. A tensor is live during half-open logical execution steps[start,end); these are ordering indices, not timestamps or wall latency.

Process tensors sorted by(start,name). A buffer becomes reusable when its previous occupant's end<=current start. From FREE buffers with capacity>=size, choose minimum(capacity,buffer_id). If none fit, allocate the next consecutive integer ID starting0 with capacity=size. Buffer capacities never grow or shrink. Return exactly assignments (list of(name,buffer_id) in processing order), capacities (list by buffer ID), reserved_bytes(sum of capacities). Buffers retain memory when free, so reserved_bytes is this allocator's total reserved memory, not the theoretical minimum live-byte peak. Empty input returns empty lists and0. Preserve inputs; malformed contracts raise ValueError.

No byte contents are copied, no in-place operation is inferred, and two simultaneously live tensors cannot alias. This is a deterministic best-fit interval allocator, not a globally optimal memory planner.
