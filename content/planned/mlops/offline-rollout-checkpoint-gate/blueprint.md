---
{
  "schema_version": 1,
  "problem_id": "offline-rollout-checkpoint-gate",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Select a Checkpoint with Offline and Rollout Gates",
  "summary": "Choose a candidate only when offline loss, rollout coverage and exact success-rate gates all pass.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "checkpoint-selection",
    "evaluation-gates"
  ],
  "paper_ids": [
    "2021-robomimic"
  ],
  "paper_sections": [
    "Stopping criteria and policy selection from offline demonstrations"
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
  "entrypoint": "solution.select_checkpoint",
  "physical_contract": "Metrics summarize evaluations under one supplied task protocol. Loss and success are dimensionless; counts are rollout episodes. No hardware command, timestamp or coordinate transform is produced.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "loss gate excludes high-success checkpoint",
      "exact success threshold equality",
      "no candidate passes"
    ],
    "hidden_case_families": [
      "rate-loss-ID selection priorities",
      "zero-trial candidates and empty collection",
      "malformed counters/bounds/rational threshold",
      "preserved inputs"
    ],
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "mlops-batch4-draft-0.1.0",
    "evaluator_sha256": null
  },
  "provenance": {
    "authoring_notes": "robomimic motivates comparing offline objectives with rollout behavior. These explicit thresholds and deterministic selection rules are an original teaching policy, not a claim about the paper's exact checkpoint selection implementation.",
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

# Select a Checkpoint with Offline and Rollout Gates

## Learning objective

Choose a candidate only when offline loss, rollout coverage and exact success-rate gates all pass.

## Source and scope

robomimic motivates comparing offline objectives with rollout behavior. These explicit thresholds and deterministic selection rules are an original teaching policy, not a claim about the paper's exact checkpoint selection implementation. Source location: Stopping criteria and policy selection from offline demonstrations. [Primary source](https://arxiv.org/abs/2108.03298).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate bounded candidate evidence; filter all three gates; select by exact success fraction, loss and ID. Sorting O(NlogN) is acceptable; a single-pass exact comparator also works.

## Evaluator plan

Public cases: loss gate excludes high-success checkpoint; exact success threshold equality; no candidate passes. Hidden cases: rate-loss-ID selection priorities; zero-trial candidates and empty collection; malformed counters/bounds/rational threshold; preserved inputs. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

