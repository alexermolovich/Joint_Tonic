---
{
  "schema_version": 1,
  "problem_id": "dataset-version-schema-drift",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Detect Dataset-Version and Schema Drift",
  "summary": "Report version and physical-schema changes without mistaking a matching shape for semantic compatibility.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "dataset-versioning",
    "schema-drift",
    "physical-metadata"
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
    "dependencies": {},
    "platform": "linux-x86_64-cpu",
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "budget_status": "actual shared worker limits; isolated Run/Submit verified"
  },
  "entrypoint": "solution.dataset_contract_drift",
  "physical_contract": "Input metadata defines each robot's channels and task protocol. The function preserves supplied meanings; no robot kinematics, coordinate conversion, clock alignment or hardware execution occurs.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "version plus unit/frame change",
      "added and removed datasets/features",
      "identical snapshots"
    ],
    "hidden_case_families": [
      "one reason per changed field and sorted order",
      "shape/dtype distinctions",
      "malformed snapshot/schema validation",
      "empty snapshots and preserved inputs"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "275fa864621b4f6e1241a0b2f84acfd7a0dd4a2612a26819cd53a7a36207d937"
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

# Detect Dataset-Version and Schema Drift

## Learning objective

Report version and physical-schema changes without mistaking a matching shape for semantic compatibility.

## Source and scope

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. Source location: SectionIV data consolidation and SectionV cross-embodiment evaluation. [Primary source](https://arxiv.org/abs/2310.08864).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate bounded metadata; compare dataset/feature key sets and all descriptor fields; emit deterministic issue tuples. O(total feature descriptors plus output sorting).

## Evaluator plan

Public cases: version plus unit/frame change; added and removed datasets/features; identical snapshots. Hidden cases: one reason per changed field and sorted order; shape/dtype distinctions; malformed snapshot/schema validation; empty snapshots and preserved inputs. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

