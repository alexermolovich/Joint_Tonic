---
{
  "schema_version": 1,
  "problem_id": "dm-control-action-repeat",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Implement Action Repeat Correctly",
  "summary": "Holding an action for several simulator transitions changes the control period.",
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
  "entrypoint": "solution.aggregate_action_repeat",
  "physical_contract": {
    "frames": [
      "Fixed caller-defined axes; no implicit coordinate transform"
    ],
    "units": {
      "rewards/reward": "task reward units",
      "discounts/discount": "dimensionless",
      "steps": "underlying transition count"
    },
    "axes": "Chronological transition vectors(T,); scalar aggregate.",
    "timestamp_assumptions": "No wall clock; transition order supplied explicitly where relevant",
    "batching": "Chronological transition vectors(T,); scalar aggregate."
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
    "evaluator_sha256": "afad0ded839673eba4f21d9d0d1a04d730251f7a7e5bc0274fc096bc41a59e27"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full simulator or benchmark reproduction. Backlog PB-245",
    "primary_urls": [
      "https://github.com/google-deepmind/dm_env/blob/master/dm_env/_environment.py"
    ],
    "paper_card": "research/papers/simulation-sim2real/2018-deepmind-control-suite.md",
    "manifest": "research/manifests/expansion-150.md"
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

# Implement Action Repeat Correctly

## Goal

Holding an action for several simulator transitions changes the control period.

## Contract

aggregate_action_repeat(rewards, discounts, last, repeat) -> dict{reward,discount,steps,last}. rewards and discounts float(T,), last bool(T,),1<=T<=100000, discounts in[0,1], rewards abs<=1e6. repeat built-in int1..T. Examine first repeat transitions, stop immediately AFTER first True in last within that prefix. For K consumed transitions, reward=sum_i(reward_i*product_{j<i}discount_j), discount=product_{i<K}discount_i, steps=Python int K, last=Python bool last[K-1]. Accumulate float64; no additional agent gamma. Validate ALL supplied arrays including unused tail values. Zero discount alone does NOT stop repeat, because LAST controls the episode boundary. Nonzero final discount allows time-limit bootstrap. This aggregates already-produced repeated-action transition evidence; it does not call a simulator or verify actions were identical.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

rewards=[1,2,99], discounts=[0.5,1,1], last=[False,True,False], repeat=3 -> {reward:2.,discount:0.5,steps:2,last:True}.

### Example 2

rewards=[3,8], discounts=[0,1], last=[False,False], repeat=2 -> {reward:3.,discount:0.,steps:2,last:False}.

## Source and scope

Original bounded component associated with [2018-deepmind-control-suite](https://github.com/google-deepmind/dm_env/blob/master/dm_env/_environment.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
