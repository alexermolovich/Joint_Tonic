---
{
  "schema_version": 1,
  "problem_id": "validation-loss-rollout-ranking",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Compare Validation Loss with Rollout Success",
  "summary": "Expose when offline-loss ordering disagrees with the ordering of observed rollout success.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "offline-evaluation",
    "rollout-success",
    "model-selection"
  ],
  "paper_ids": [
    "2021-robomimic"
  ],
  "paper_sections": [
    "Offline demonstration evaluation and stopping criteria"
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
  "entrypoint": "solution.compare_checkpoint_metrics",
  "physical_contract": "Batch items are independent episodes or evaluation records. Action channels preserve upstream units, coordinate frames and control ordering; no timing or physical quantity is inferred. Scalar loss and success metrics are dimensionless under supplied evaluation contracts.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "opposite offline and rollout winners",
      "exact rational tie with ID tiebreak",
      "single checkpoint"
    ],
    "hidden_case_families": [
      "integer ratio ordering and stable ties",
      "malformed records and finite loss",
      "large candidate set and preservation"
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
    "authoring_notes": "robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system.",
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

# Compare Validation Loss with Rollout Success

## Learning objective

Expose when offline-loss ordering disagrees with the ordering of observed rollout success.

## Source and scope

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. Source location: Offline demonstration evaluation and stopping criteria. [Primary source](https://arxiv.org/abs/2108.03298).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate records, sort once by(loss,ID) and once by exact descending success fraction thenID; return the two ID lists and winner disagreement. Use exact rational arithmetic or integer comparison, O(NlogN).

## Evaluator plan

Public cases: opposite offline and rollout winners; exact rational tie with ID tiebreak; single checkpoint. Hidden cases: integer ratio ordering and stable ties; malformed records and finite loss; large candidate set and preservation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

