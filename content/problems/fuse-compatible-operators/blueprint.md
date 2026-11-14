---
{
  "schema_version": 1,
  "problem_id": "fuse-compatible-operators",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Fuse Compatible Operators in a Compute Graph",
  "summary": "Fuse Compatible Operators in a Compute Graph",
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
  "entrypoint": "solution.fuse_operator_chains",
  "physical_contract": {
    "frames": [
      "No spatial transform; named records retain their supplied identity"
    ],
    "units": {
      "shape": "dimensionless tensor extents",
      "nodes": "logical operators; no measured hardware time"
    },
    "axes": "Each shape has 1\u20134 axes; a fusible chain preserves all extents.",
    "timestamp_assumptions": "No wall-clock timestamps; deterministic logical inputs only.",
    "batching": "Each shape has 1\u20134 axes; a fusible chain preserves all extents."
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
    "evaluator_sha256": "19751ea33b2177eab4ff45761881744c101d6080b1853fe226b59b2bcc7078b7",
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

# Fuse Compatible Operators in a Compute Graph

Implement fuse_operator_chains(nodes) -> list[tuple[str,...]].

nodes is a Python list of 0–10000 tuples(id,op,parent,shape) in topological order. IDs match ASCII [a-z][a-z0-9_-]{0,63} and are unique. op is input,scale,relu,sigmoid or barrier. input requires parent=None; every other op has exactly one earlier node ID as parent. shape is a tuple of 1–4 built-in non-bool ints in [1,4096]; its product <=1000000. A child may declare a different shape only when its op is barrier. Inputs and barriers are never fused.

Partition every node into groups. Fuse a fusible child(scale,relu,sigmoid) into its parent's group iff the parent is also fusible and has exactly one direct consumer in the COMPLETE graph. Otherwise start a new group. Group members follow input/topological order; groups are ordered by the first member's input position. Return fresh tuples in a fresh list. Empty graph returns[]. Preserve inputs. Invalid containers, labels, dimensions, duplicate IDs, forward/missing references or unsupported shape changes raise ValueError.

This conservative unary-chain partition does not execute tensors, combine arbitrary branches, reorder computations, or claim TVM's full fusion algorithm. The same declared shape means the same caller-supplied layout/dtype; this function does not infer equivalence across layouts.
