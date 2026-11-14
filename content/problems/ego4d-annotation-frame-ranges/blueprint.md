---
{
  "schema_version": 1,
  "problem_id": "ego4d-annotation-frame-ranges",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Align Egocentric Video Annotations",
  "summary": "Variable-frame-rate video cannot be aligned reliably with a nominal FPS multiplication.",
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
  "entrypoint": "solution.annotation_frame_ranges",
  "physical_contract": {
    "frames": [
      "Caller-declared physical frames; no inferred transforms"
    ],
    "units": {
      "timestamps/endpoints": "integer nanoseconds on one source-video clock",
      "returned ranges": "half-open frame indices"
    },
    "axes": "Frame times(T,),annotation intervals(A,2),output(A,2),input annotation order preserved.",
    "timestamp_assumptions": "Integer nanoseconds on source-video clock where applicable; no wall clock",
    "batching": "Frame times(T,),annotation intervals(A,2),output(A,2),input annotation order preserved."
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
    "evaluator_sha256": "706bfc339eaa61cba56b69c94de1ff535a70ddbe41dbec00eef5f0d03d539b20"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded operational teaching component. Backlog PB-012",
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

# Align Egocentric Video Annotations

## Contract

annotation_frame_ranges(frame_times_ns, intervals_ns) -> ndarray. frame_times_ns int64(T,),0<=T<=1000000, nonnegative strictly increasing on one source-video clock. intervals_ns int64(A,2),0<=A<=100000, nonnegative start<end. Treat annotations as half-open [start,end) intervals; return int64(A,2) frame-index ranges[lo,hi) containing timestamps start<=t<end, using insertion positions. Intervals can overlap or lie outside video coverage; empty matches return equal insertion indices, not(-1,-1). Preserve input interval order. No constant-frame-rate assumption; no exposure integration or temporal-IoU metric. Inputs belong to one source video; multi-video identity must be handled before calling.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

frame_times[0,10,25,40],intervals[[10,40],[11,24],[50,60]] -> [[1,3],[2,2],[4,4]].

### Example 2

empty timestamps and intervals[[0,1]] -> [[0,0]].

## Source and scope

Original bounded component associated with [2021-ego4d](https://arxiv.org/abs/2110.07058). It does not reproduce the full dataset loader, task suite or headline results.
