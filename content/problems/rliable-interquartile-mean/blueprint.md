---
{
  "schema_version": 1,
  "problem_id": "rliable-interquartile-mean",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute an Interquartile Mean Benchmark Score",
  "summary": "A few exceptionally lucky or unlucky training seeds can dominate an ordinary mean.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "simulation-evaluation",
    "2021-rliable-statistical-precipice"
  ],
  "paper_ids": [
    "2021-rliable-statistical-precipice"
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
  "entrypoint": "solution.interquartile_score",
  "physical_contract": {
    "frames": [
      "Fixed caller-defined axes; no implicit coordinate transform"
    ],
    "units": {
      "scores": "dimensionless normalized task returns"
    },
    "axes": "Scores(M,N): task,run; pooled sorted(K,).",
    "timestamp_assumptions": "No wall clock; transition order supplied explicitly where relevant",
    "batching": "Scores(M,N): task,run; pooled sorted(K,)."
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
    "evaluator_sha256": "3f66f2a8917a3d530eea7bff0a21f69b1e4346cfd87307099c8534cb512595b4"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full simulator or benchmark reproduction. Backlog PB-129",
    "primary_urls": [
      "https://github.com/google-research/rliable/blob/master/rliable/metrics.py"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2021-rliable-statistical-precipice.md",
    "manifest": "research/manifests/balanced-expansion-156.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root",
    "research_curator",
    "perception_completion"
  ]
}
---

# Compute an Interquartile Mean Benchmark Score

## Goal

A few exceptionally lucky or unlucky training seeds can dominate an ordinary mean.

## Contract

interquartile_score(scores) -> float. scores is float32/64(M,N), 1<=M,N<=2048, M*N<=1000000, dimensionless already-normalized scores with task rows and independent training-seed columns. Pool all scores, sort, remove floor(M*N/4) from EACH end, average remaining. This pins the finite-sample convention used by rliable's 25%-trimmed mean; it does not fractionally trim boundaries or trim each task separately. All tasks have the same run count. Work O(K log K), storage O(K), K=M*N.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

[[0,1,2,3],[4,5,6,100]] -> 3.5; sorted middle is [2,3,4,5].

### Example 2

[[1,2,100]] -> 103/3; floor(3/4)=0 so all three scores remain.

## Source and scope

Original bounded component associated with [2021-rliable-statistical-precipice](https://github.com/google-research/rliable/blob/master/rliable/metrics.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
