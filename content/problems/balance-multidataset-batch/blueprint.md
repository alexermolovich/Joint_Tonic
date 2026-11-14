---
{
  "schema_version": 1,
  "problem_id": "balance-multidataset-batch",
  "content_version": "1.0.0",
  "status": "implemented",
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
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "0c8d44bcc254b5c7adfe4838ecd163ab97c6da0fe5c4197540e527bbfcf45456"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:0c8d44bcc254b5c7adfe4838ecd163ab97c6da0fe5c4197540e527bbfcf45456",
    "evaluator_sha256": "0c8d44bcc254b5c7adfe4838ecd163ab97c6da0fe5c4197540e527bbfcf45456",
    "generated_fixture_hash": "0c8d44bcc254b5c7adfe4838ecd163ab97c6da0fe5c4197540e527bbfcf45456"
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
  "reviewers": [
    "perception_implementation"
  ],
  "derived_draft_version": "0.1.0"
}
---

# Balance a Multi-Dataset Training Mixture

## Learning objective

Allocate one bounded batch across datasets according to configured weights with exact deterministic rounding.

## Source and scope

Open X-Embodiment motivates deliberate mixture composition. Hamilton largest-remainder allocation is an original deterministic batch-construction exercise, not a claim that RT-X uses this exact sampler. Source location: SectionIV training data mixture; exact apportionment is an original teaching choice. [Primary source](https://arxiv.org/abs/2310.08864).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate integer weights and batch size; compute exact floor quotas; allocate R extras by sorted remainder/ID; emit sorted counts. O(KlogK) time and O(K) space.

## Evaluator plan

Public cases: equal weights and deterministic remainder tie; unequal weights including zero weight; zero-sized batch. Hidden cases: exact integer remainder arithmetic; large weights and batch size; typed bounds and positive-total requirement; stable source order and preservation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

