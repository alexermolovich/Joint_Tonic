---
{
  "schema_version": 1,
  "problem_id": "dm-control-tolerance-reward",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Evaluate a Bounded Continuous-Control Reward",
  "summary": "A tolerance reward distinguishes a target interval from a smoothly decaying neighborhood around it.",
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
  "entrypoint": "solution.tolerance_reward",
  "physical_contract": {
    "frames": [
      "Fixed caller-defined axes; no implicit coordinate transform"
    ],
    "units": {
      "values/bounds/margin": "one supplied task-coordinate unit",
      "reward": "dimensionless [0,1]"
    },
    "axes": "Values(N,), scalar bounds/margin, output(N,).",
    "timestamp_assumptions": "No wall clock; transition order supplied explicitly where relevant",
    "batching": "Values(N,), scalar bounds/margin, output(N,)."
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
    "evaluator_sha256": "d7fbf5fdc6f1ab4ad49d7d001654253c0dff3b3ec493101036b10368e25cc1ab"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full simulator or benchmark reproduction. Backlog PB-196",
    "primary_urls": [
      "https://github.com/google-deepmind/dm_control/blob/main/dm_control/utils/rewards.py"
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

# Evaluate a Bounded Continuous-Control Reward

## Goal

A tolerance reward distinguishes a target interval from a smoothly decaying neighborhood around it.

## Contract

tolerance_reward(values, lower, upper, margin, value_at_margin) -> ndarray. values float(N,),0<=N<=1000000. lower/upper finite scalar abs<=1e6 with lower<=upper; margin scalar in[0,1e6], value_at_margin scalar in[1e-6,1-1e-6]. Values and bounds share ONE declared task coordinate unit (e.g meters); margin shares that unit; no coordinate transforms. Let d=max(lower-x,0,x-upper). If margin=0, output1 when d=0 else0. Otherwise output exp(log(value_at_margin)*(d/margin)^2); return1 exactly when d=0. Clamp normalized distance to1e6 BEFORE squaring so extremely tiny positive margin yields0 for distant finite values without overflow/NaN; output float64(N,). This selects the Gaussian tolerance family only, not every dm_control sigmoid or task composition.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

values=[-1,0,1,2], lower=0,upper=1,margin=1,value_at_margin=0.5 -> [0.5,1,1,0.5].

### Example 2

values=[-1,0,1], lower=upper=0,margin=0,value_at_margin=0.5 -> [0,1,0].

## Source and scope

Original bounded component associated with [2018-deepmind-control-suite](https://github.com/google-deepmind/dm_control/blob/main/dm_control/utils/rewards.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
