---
{
  "schema_version": 1,
  "problem_id": "mask-unavailable-action-dimensions",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Mask Unavailable Action Dimensions",
  "summary": "Replace unavailable action channels with zeros without letting invalid placeholder values contaminate valid data.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "cross-embodiment",
    "action-masks"
  ],
  "paper_ids": [
    "2024-open-x-embodiment"
  ],
  "paper_sections": [
    "SectionIV data consolidation and SectionV cross-embodiment evaluation"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; baseline worker exists",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "platform": "linux-x86_64-cpu",
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "budget_status": "actual shared worker limits; isolated Run/Submit verified"
  },
  "entrypoint": "solution.mask_action_dimensions",
  "physical_contract": "Input metadata defines each robot's channels and task protocol. The function preserves supplied meanings; no robot kinematics, coordinate conversion, clock alignment or hardware execution occurs.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "different available channels per robot",
      "masked NaN/infinity placeholders",
      "empty batch"
    ],
    "hidden_case_families": [
      "all unavailable rows and valid zero",
      "noncontiguous input/output ownership",
      "shape/dtype/value bounds"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "2c349dd89bbacab917bed8bc169ee4f780381ac098d6b9275a15e6a21f7733a7"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "mlops-batch5-draft-0.1.0",
    "evaluator_sha256": null
  },
  "provenance": {
    "authoring_notes": "Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.08864"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2024-open-x-embodiment.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "code_issue_scout"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Mask Unavailable Action Dimensions

## Learning objective

Replace unavailable action channels with zeros without letting invalid placeholder values contaminate valid data.

## Source and scope

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. Source location: SectionIV data consolidation and SectionV cross-embodiment evaluation. [Primary source](https://arxiv.org/abs/2310.08864).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate NumPy arrays and matching shapes; check available values only; create zero output and assign valid positions. O(BD) time and memory.

## Evaluator plan

Public cases: different available channels per robot; masked NaN/infinity placeholders; empty batch. Hidden cases: all unavailable rows and valid zero; noncontiguous input/output ownership; shape/dtype/value bounds. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

