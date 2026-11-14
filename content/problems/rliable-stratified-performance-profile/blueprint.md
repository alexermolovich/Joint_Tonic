---
{
  "schema_version": 1,
  "problem_id": "rliable-stratified-performance-profile",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Bootstrap a Stratified Performance Profile",
  "summary": "A performance profile asks what fraction of runs clear each score threshold.",
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
  "entrypoint": "solution.stratified_profile",
  "physical_contract": {
    "frames": [
      "Fixed caller-defined axes; no implicit coordinate transform"
    ],
    "units": {
      "scores/thresholds": "dimensionless normalized task returns",
      "indices": "within-task run indices"
    },
    "axes": "Scores(M,N),indices(B,M,N),thresholds(Q,),profiles(Q,) and(B,Q).",
    "timestamp_assumptions": "No wall clock; transition order supplied explicitly where relevant",
    "batching": "Scores(M,N),indices(B,M,N),thresholds(Q,),profiles(Q,) and(B,Q)."
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
    "evaluator_sha256": "7a55de5f1c1783d1864dc76071bd113c3c01aa222596270d301f05d950bb372b"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full simulator or benchmark reproduction. Backlog PB-047",
    "primary_urls": [
      "https://arxiv.org/abs/2108.13264"
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

# Bootstrap a Stratified Performance Profile

## Goal

A performance profile asks what fraction of runs clear each score threshold.

## Contract

stratified_profile(scores, thresholds, resample_indices) -> dict{profile,replicates}. scores float(M,N),1<=M,N<=256. thresholds float(Q,),0<=Q<=128, arbitrary order/duplicates retained. resample_indices int64(B,M,N),0<=B<=512, each index in[0,N), at most1e6 indices and B*M*N*max(Q,1)<=2e7. Bootstrap replicate b independently gathers N supplied indices within each TASK row; task rows themselves are fixed, never pooled or resampled. Return profile float64(Q,) = mean(scores>threshold), replicates float64(B,Q) from gathered scores. Strict >, not >=. Supplied resampling indices make the exercise replayable without RNG; this computes empirical replicate curves, not percentile intervals or coverage guarantees. O((B+1)*M*N*Q), avoid allocating B*M*N*Q at once.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

scores=[[0,2],[10,12]], thresholds=[2,10], indices=[[[1,1],[0,0]]] -> profile=[0.5,0.25], replicates=[[0.5,0]].

### Example 2

scores=[[1]], thresholds=[1,0,1], indices shape(0,1,1) -> profile=[0,1,0], replicates shape(0,3).

## Source and scope

Original bounded component associated with [2021-rliable-statistical-precipice](https://arxiv.org/abs/2108.13264). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
