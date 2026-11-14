---
{
  "schema_version": 1,
  "problem_id": "balance-multidataset-batch",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Balance a Multi-Dataset Training Mixture",
  "summary": "Allocate one bounded batch across datasets according to configured weights with exact deterministic rounding.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "dataset-mixtures",
    "sampling-policy",
    "reproducibility"
  ],
  "paper_ids": [
    "2024-open-x-embodiment"
  ],
  "paper_sections": [
    "SectionIV training data mixture; exact apportionment is an original teaching choice"
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
  "entrypoint": "solution.allocate_dataset_batch",
  "physical_contract": "Dataset weights and batch counts are dimensionless. The caller defines whether one item is an episode or transition; this function allocates counts without drawing data, changing frames or estimating durations.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "equal weights and deterministic remainder tie",
      "unequal weights including zero weight",
      "zero-sized batch"
    ],
    "hidden_case_families": [
      "exact integer remainder arithmetic",
      "large weights and batch size",
      "typed bounds and positive-total requirement",
      "stable source order and preservation"
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
    "authoring_notes": "Open X-Embodiment motivates deliberate mixture composition. Hamilton largest-remainder allocation is an original deterministic batch-construction exercise, not a claim that RT-X uses this exact sampler.",
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
  "reviewers": ["perception_implementation"]
}
---

# Balance a Multi-Dataset Training Mixture

## Learning objective

Allocate one bounded batch across datasets according to configured weights with exact deterministic rounding.

## Source and scope

Open X-Embodiment motivates deliberate mixture composition. Hamilton largest-remainder allocation is an original deterministic batch-construction exercise, not a claim that RT-X uses this exact sampler. Source location: SectionIV training data mixture; exact apportionment is an original teaching choice. [Primary source](https://arxiv.org/abs/2310.08864).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate integer weights and batch size; compute exact floor quotas; allocate R extras by sorted remainder/ID; emit sorted counts. O(KlogK) time and O(K) space.

## Evaluator plan

Public cases: equal weights and deterministic remainder tie; unequal weights including zero weight; zero-sized batch. Hidden cases: exact integer remainder arithmetic; large weights and batch size; typed bounds and positive-total requirement; stable source order and preservation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

