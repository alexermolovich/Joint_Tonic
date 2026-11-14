---
{
  "schema_version": 1,
  "problem_id": "batch-variable-robot-episodes",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Batch Variable-Length Episodes with Masks",
  "summary": "Pad complete robot episodes to a shared horizon without confusing valid zeros with padding.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "offline-demonstrations",
    "padding",
    "episode-boundaries"
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
    "solution_dependencies": [
      "numpy"
    ]
  },
  "entrypoint": "solution.batch_episodes",
  "physical_contract": "Batch items are independent episodes or evaluation records. Action channels preserve upstream units, coordinate frames and control ordering; no timing or physical quantity is inferred. Scalar loss and success metrics are dimensionless under supplied evaluation contracts.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "unequal episode lengths",
      "empty episode with valid zero",
      "all-empty episodes"
    ],
    "hidden_case_families": [
      "noncontiguous storage and shapes",
      "dtype/value/width contract",
      "declared padded-size budget"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "216c2c501de19967e00496bfd2dcfb1c33f256d79d730a10c7cde5745ce5444f"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:216c2c501de19967e00496bfd2dcfb1c33f256d79d730a10c7cde5745ce5444f",
    "evaluator_sha256": "216c2c501de19967e00496bfd2dcfb1c33f256d79d730a10c7cde5745ce5444f",
    "generated_fixture_hash": "216c2c501de19967e00496bfd2dcfb1c33f256d79d730a10c7cde5745ce5444f"
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

# Batch Variable-Length Episodes with Masks

## Learning objective

Pad complete robot episodes to a shared horizon without confusing valid zeros with padding.

## Source and scope

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. Source location: Offline demonstration evaluation and stopping criteria. [Primary source](https://arxiv.org/abs/2108.03298).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate bounded float64 arrays and shared width; allocate batch, mask and lengths; copy prefixes. Time O(BLD), memory O(BLD), with padded allocation explicitly bounded.

## Evaluator plan

Public cases: unequal episode lengths; empty episode with valid zero; all-empty episodes. Hidden cases: noncontiguous storage and shapes; dtype/value/width contract; declared padded-size budget. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

