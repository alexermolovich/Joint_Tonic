---
{
  "schema_version": 1,
  "problem_id": "scene-safe-trajectory-split",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Split Robot Trajectories Without Scene Leakage",
  "summary": "Assign complete scenes to deterministic train or validation partitions while preserving trajectory order.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "offline-demonstrations",
    "scene-leakage",
    "evaluation"
  ],
  "paper_ids": [
    "2021-robomimic"
  ],
  "paper_sections": [
    "Evaluation and dataset design; scene-grouped hashing is an original teaching protocol"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; baseline worker exists",
    "dependencies": {},
    "platform": "linux-x86_64-cpu",
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "budget_status": "actual shared worker limits; this draft has not run"
  },
  "entrypoint": "solution.split_trajectories_by_scene",
  "physical_contract": "No pose or signal arrays are consumed. Episode IDs identify complete trajectories and supplied scene IDs identify shared environments. No clock, frame or physical unit is inferred. One output partition per episode; one shared decision per scene.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "two scenes with interleaved episodes",
      "empty collection and boundary thresholds",
      "seeded stable scene assignment"
    ],
    "hidden_case_families": [
      "input-order preservation and episode uniqueness",
      "all episodes of a scene stay together",
      "invalid typed bounds and mismatched lengths",
      "large repeated-scene collection"
    ],
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "mlops-batch3-draft-0.1.0",
    "evaluator_sha256": null
  },
  "provenance": {
    "authoring_notes": "robomimic motivates careful evaluation of offline robot demonstrations. Grouping by supplied scene identity and the exact SHA-256 bucket protocol are original teaching choices, not a split algorithm claimed by the paper.",
    "primary_urls": [
      "https://arxiv.org/abs/2108.03298"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2021-robomimic.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "code_issue_scout"
  ],
  "reviewers": ["perception_implementation"]
}
---

# Split Robot Trajectories Without Scene Leakage

## Learning objective

Assign complete scenes to deterministic train or validation partitions while preserving trajectory order.

## Source and scope

robomimic motivates careful evaluation of offline robot demonstrations. Grouping by supplied scene identity and the exact SHA-256 bucket protocol are original teaching choices, not a split algorithm claimed by the paper. Source location: Evaluation and dataset design; scene-grouped hashing is an original teaching protocol. [Primary source](https://arxiv.org/abs/2108.03298).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate names and scalar bounds; memoize exact SHA-256 bucket decisions by scene; append episodes in original order. Complexity O(N+S) for N episodes and S unique scenes, with bounded ID lengths.

## Evaluator plan

Public cases: two scenes with interleaved episodes; empty collection and boundary thresholds; seeded stable scene assignment. Hidden cases: input-order preservation and episode uniqueness; all episodes of a scene stay together; invalid typed bounds and mismatched lengths; large repeated-scene collection. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

