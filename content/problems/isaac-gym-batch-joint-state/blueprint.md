---
{
  "schema_version": 1,
  "problem_id": "isaac-gym-batch-joint-state",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Batch Independent Simulator States",
  "summary": "Simulator state is often exposed as a flattened buffer.",
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
    "2021-isaac-gym"
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
  "entrypoint": "solution.batch_joint_states",
  "physical_contract": {
    "frames": [
      "Fixed caller-defined axes; no implicit coordinate transform"
    ],
    "units": {
      "state[...,0]": "radians",
      "state[...,1]": "radians/second",
      "indices": "flat joint-buffer row indices"
    },
    "axes": "Flat state(A,2),indices(B,J),output(B,J,2).",
    "timestamp_assumptions": "No wall clock; transition order supplied explicitly where relevant",
    "batching": "Flat state(A,2),indices(B,J),output(B,J,2)."
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
    "evaluator_sha256": "8e2a102da47559926c5df71c2cc7dc42814aabd1009ff165c35004f8a194b5d6"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full simulator or benchmark reproduction. Backlog PB-046",
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

# Batch Independent Simulator States

## Goal

Simulator state is often exposed as a flattened buffer.

## Contract

batch_joint_states(flat_state, dof_indices) -> ndarray. flat_state float(A,2),0<=A<=100000, column0 joint position radians and column1 angular velocity radians/second. dof_indices int64(B,J),0<=B<=4096,1<=J<=256,B*J<=A and <=100000. Every selected index must be unique across ALL environments, in[0,A). Return float64(B,J,2) in given row/column order, fresh copy, no assumption rows are contiguous actors. Unselected flat rows are permitted and still validated. Empty B accepted even if A=0. This is a simplified homogeneous revolute-joint buffer gather, not an Isaac Gym actor API or prismatic/rigid-body layout.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

flat_state=[[1,10],[2,20],[3,30],[4,40]], indices=[[2,0],[3,1]] -> [[[3,30],[1,10]],[[4,40],[2,20]]].

### Example 2

flat_state shape(0,2), indices shape(0,3) -> shape(0,3,2). Repeated selected index raises ValueError.

## Source and scope

Original bounded component associated with [2021-isaac-gym](https://arxiv.org/abs/2108.10470). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
