---
{
  "schema_version": 1,
  "problem_id": "libero-semantic-scene-factors",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Separate Task Semantics from Scene Variation",
  "summary": "The same manipulation goal can appear in different scenes.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "dataset-evaluation",
    "2023-libero"
  ],
  "paper_ids": [
    "2023-libero"
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
  "entrypoint": "solution.semantic_scene_groups",
  "physical_contract": {
    "frames": [
      "Caller-declared physical frames; no inferred transforms"
    ],
    "units": {
      "semantic and scene fields": "categorical identities",
      "has_scene_variation": "Boolean evidence of multiple declared scenes"
    },
    "axes": "Task records -> one group per ordered(verb,object,goal), sorted task IDs and unique scene IDs.",
    "timestamp_assumptions": "Integer nanoseconds on source-video clock where applicable; no wall clock",
    "batching": "Task records -> one group per ordered(verb,object,goal), sorted task IDs and unique scene IDs."
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
    "evaluator_sha256": "605975f5bc9cf90daf61cbe66f75d562cba171889e45d6fe4eff98fd059822e1"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded operational teaching component. Backlog PB-381",
    "primary_urls": [
      "https://arxiv.org/abs/2306.03310"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2023-libero.md",
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

# Separate Task Semantics from Scene Variation

## Contract

semantic_scene_groups(records) -> list[dict]. records list of0..10000 exact records{task_id,verb,object_id,goal_id,scene_id}, all common identifiers, unique task_id. A semantic key is the ORDERED tuple(verb,object_id,goal_id); scene_id is excluded. Return exact records{semantic_key,task_ids,scene_ids,has_scene_variation}, sorted lexically by semantic_key, with task_ids sorted and scene_ids sorted UNIQUE. has_scene_variation is True iff at least2 distinct scenes occur in that semantic group. Repeated scene IDs across different semantic groups do not merge them; two task IDs with same semantics and scene are valid distinct tasks. No language parsing or geometry is inferred. This indexes provided factor annotations rather than reproducing LIBERO task taxonomy.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

tasks a(pick,cup,tray,kitchen),b(pick,cup,tray,lab),c(place,cup,tray,kitchen) -> group(pick,cup,tray):tasks[a,b],scenes[kitchen,lab],True; group(place,cup,tray):tasks[c],scenes[kitchen],False.

### Example 2

Two tasks a,b both(pick,cup,tray,kitchen) -> one group,task_ids[a,b],scene_ids[kitchen],has_scene_variationFalse.

## Source and scope

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). It does not reproduce the full dataset loader, task suite or headline results.
