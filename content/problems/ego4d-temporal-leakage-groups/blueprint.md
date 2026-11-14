---
{
  "schema_version": 1,
  "problem_id": "ego4d-temporal-leakage-groups",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Build Leakage-Safe Temporal Splits",
  "summary": "Adjacent clips can share nearly identical context even when they do not overlap.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "dataset-evaluation",
    "2021-ego4d"
  ],
  "paper_ids": [
    "2021-ego4d"
  ],
  "paper_sections": [
    "Mechanism explicitly scoped in the contract"
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
  "entrypoint": "solution.temporal_split_groups",
  "physical_contract": {
    "frames": [
      "Caller-declared physical frames; no inferred transforms"
    ],
    "units": {
      "interval endpoints/guard": "integer nanoseconds on each source video clock",
      "IDs": "source-video and clip identities"
    },
    "axes": "Clip records -> connected groups within video -> sorted per-clip split rows.",
    "timestamp_assumptions": "Integer nanoseconds on source-video clock where applicable; no wall clock",
    "batching": "Clip records -> connected groups within video -> sorted per-clip split rows."
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
    "evaluator_sha256": "4b243d12dbf334dd7571d996614223b4000df32dd00fa7d6d33175fd95876c53"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded operational teaching component. Backlog PB-070",
    "primary_urls": [
      "https://arxiv.org/abs/2110.07058"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2021-ego4d.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Build Leakage-Safe Temporal Splits

## Contract

temporal_split_groups(clips, heldout_ids, guard_ns) -> list[dict]. clips list0..100000 exact records{clip_id,video_id,start_ns,end_ns}; common IDs,unique clip_id; endpoints built-in int0..2^63-1,start<end. heldout_ids list of unique declared clip IDs (empty allowed),guard_ns built-in int0..2^63-1. Within SAME video, connect two clips when their interval distance gap=max(0,max(starts)-min(ends))<=guard_ns. Thus overlapping AND merely touching intervals connect at guard0. Take transitive connected components; components never cross video IDs. Group ID is lexical-smallest clip_id; split is test iff component contains any heldoutID else train. Return exact{clip_id,group_id,split} sorted by clip_id. Use interval sweep rather than quadratic pair checking at scale; arithmetic uses Python integers. This original guard-band split policy does not solve person/scene leakage across distinct videos.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

same-video a[0,10),b[10,20),c[21,30),heldout[b],guard0 -> a,b groupa/test; c groupc/train.

### Example 2

same-video a[0,10),b[15,20),c[25,30),heldout[c],guard5 -> all groupa/test through transitive connections.

## Source and scope

Original bounded component associated with [2021-ego4d](https://arxiv.org/abs/2110.07058). It does not reproduce the full dataset loader, task suite or headline results.
