---
{
  "schema_version": 1,
  "problem_id": "validation-loss-rollout-ranking",
  "content_version": "1.0.0",
  "status": "implemented",
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
    "image_status": "pending OCI build; actual local bubblewrap Run and Submit verified",
    "dependencies": {
      "numpy": "2.2.4",
      "torch": "2.6.0+cpu"
    },
    "platform": "linux-x86_64-cpu",
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "budget_status": "actual shared worker caps; per-process address-space limit",
    "solution_dependencies": []
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
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "1541052960d43d86d6e35556791481902dd371d9f1d5ec6429b86e10a46d4f6a"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:1541052960d43d86d6e35556791481902dd371d9f1d5ec6429b86e10a46d4f6a",
    "evaluator_sha256": "1541052960d43d86d6e35556791481902dd371d9f1d5ec6429b86e10a46d4f6a",
    "generated_fixture_hash": "1541052960d43d86d6e35556791481902dd371d9f1d5ec6429b86e10a46d4f6a"
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
  "reviewers": [
    "perception_implementation"
  ],
  "derived_draft_version": "0.1.0"
}
---

# Compare Validation Loss with Rollout Success

## Learning objective

Expose when offline-loss ordering disagrees with the ordering of observed rollout success.

## Source and scope

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. Source location: Offline demonstration evaluation and stopping criteria. [Primary source](https://arxiv.org/abs/2108.03298).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate records, sort once by(loss,ID) and once by exact descending success fraction thenID; return the two ID lists and winner disagreement. Use exact rational arithmetic or integer comparison, O(NlogN).

## Evaluator plan

Public cases: opposite offline and rollout winners; exact rational tie with ID tiebreak; single checkpoint. Hidden cases: integer ratio ordering and stable ties; malformed records and finite loss; large candidate set and preservation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

