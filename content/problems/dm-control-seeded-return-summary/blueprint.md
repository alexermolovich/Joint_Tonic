---
{
  "schema_version": 1,
  "problem_id": "dm-control-seeded-return-summary",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Aggregate Seeded Benchmark Returns",
  "summary": "A training seed with many recorded evaluation episodes should not silently receive more weight than another seed.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "simulation-evaluation",
    "2018-deepmind-control-suite"
  ],
  "paper_ids": [
    "2018-deepmind-control-suite"
  ],
  "paper_sections": [
    "Selected operational or evaluation mechanism; simplified scope in Theory"
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
  "entrypoint": "solution.seeded_return_summary",
  "physical_contract": {
    "frames": [
      "Fixed caller-defined axes; no implicit coordinate transform"
    ],
    "units": {
      "returns/means": "same supplied return units",
      "task/seed IDs": "opaque exact integer identities"
    },
    "axes": "Episode vectors(E,); sorted task/seed grid(M,S).",
    "timestamp_assumptions": "No wall clock; transition order supplied explicitly where relevant",
    "batching": "Episode vectors(E,); sorted task/seed grid(M,S)."
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
    "evaluator_sha256": "615b270301e0ef78ecf4c4f736ca389504952206aa3035b35a2cefd68fbb7700"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full simulator or benchmark reproduction. Backlog PB-007",
    "primary_urls": [
      "https://arxiv.org/abs/1801.00690"
    ],
    "paper_card": "research/papers/simulation-sim2real/2018-deepmind-control-suite.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Aggregate Seeded Benchmark Returns

## Goal

A training seed with many recorded evaluation episodes should not silently receive more weight than another seed.

## Contract

seeded_return_summary(task_ids, seed_ids, returns) -> dict{task_ids,seeds,counts,means,task_means,overall}. task_ids and seed_ids int64(E,), values0..2^63-1; returns float(E,),0<=E<=100000, finite abs<=1e6. Multiple episodes per(task,seed) are valid. Return sorted unique task_ids int64(M,), seeds int64(S,), counts int64(M,S), means float64(M,S) with NaN at missing cells. task_means float64(M,) averages PRESENT seed means equally (not all episodes); overall Python float averages task_means equally. Empty input yields empty arrays including(0,0) and overallNaN. Require M*S<=1e6. All returns use the same supplied reward/horizon convention. This exposes unequal evaluation episode counts rather than letting prolific seeds dominate; it does not estimate variance or replace IQM.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

task_ids=[0,0,0,1],seed_ids=[1,1,2,1],returns=[0,2,9,4] -> tasks[0,1],seeds[1,2],counts[[2,1],[1,0]],means[[1,9],[4,NaN]],task_means[5,4],overall4.5.

### Example 2

task_ids=[2,2],seed_ids=[7,7],returns=[-1,1] -> counts[[2]],means[[0]],task_means[0],overall0.

## Source and scope

Original bounded component associated with [2018-deepmind-control-suite](https://arxiv.org/abs/1801.00690). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
