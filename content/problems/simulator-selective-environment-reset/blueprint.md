---
{
  "schema_version": 1,
  "problem_id": "simulator-selective-environment-reset",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Reset Completed Environments Selectively",
  "summary": "Only completed environments should restart.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "simulation-evaluation",
    "2021-isaac-gym"
  ],
  "paper_ids": [
    "2021-isaac-gym",
    "2021-brax"
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
  "entrypoint": "solution.reset_environment_batch",
  "physical_contract": {
    "frames": [
      "Fixed caller-defined axes; no implicit coordinate transform"
    ],
    "units": {
      "state": "matching caller-defined per-column units and frames",
      "episode_ids/steps": "dimensionless integer counters"
    },
    "axes": "State/reset(B,D); mask/counters(B,); outputs retain batch order.",
    "timestamp_assumptions": "No wall clock; transition order supplied explicitly where relevant",
    "batching": "State/reset(B,D); mask/counters(B,); outputs retain batch order."
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
    "evaluator_sha256": "7331311279ab01b59b37fff269c1e817891a4191bd494587e6fcd6ce17e4d80d"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full simulator or benchmark reproduction. Backlog PB-342,PB-441",
    "primary_urls": [
      "https://arxiv.org/abs/2108.10470"
    ],
    "paper_card": "research/papers/simulation-sim2real/2021-isaac-gym.md",
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

# Reset Completed Environments Selectively

## Goal

Only completed environments should restart.

## Contract

reset_environment_batch(state, reset_state, done, episode_ids, steps) -> dict{state,episode_ids,steps}. state/reset_state float(B,D),0<=B<=4096,1<=D<=256,B*D<=1e6; finite abs<=1e6 including unselected rows. done bool(B,), episode_ids and steps int64(B,), each0..2^63-1. Each state column has its caller-declared unit/frame and reset_state matches it. Return state row from reset_state iff done else original state; episode_ids increment by1 only where done; steps become0 where done and otherwise remain unchanged (this is reset, not simulation step). Overflow if a selected episode_id equals int64max raises ValueError; unselected max IDs are allowed. Outputs fresh float64 state/int64 counters; inputs preserved. This is a pure batch reset bookkeeping exercise, not randomized initialization, recurrent-memory reset or a simulator API call.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

state=[[1,2],[3,4]],reset_state=[[0,0],[9,9]],done=[True,False],episode_ids=[4,8],steps=[10,20] -> state[[0,0],[3,4]],episode_ids[5,8],steps[0,20].

### Example 2

done=[False],episode_ids=[2^63-1],steps=[7] preserves both counters and the original state row.

## Source and scope

Original bounded component associated with [2021-isaac-gym](https://arxiv.org/abs/2108.10470). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
