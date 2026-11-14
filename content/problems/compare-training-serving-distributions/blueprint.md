---
{
  "schema_version": 1,
  "problem_id": "compare-training-serving-distributions",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compare Training and Serving Distributions",
  "summary": "Compare aligned categorical frequencies while distinguishing distribution shift from dataset size.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "distribution-skew",
    "robot-data"
  ],
  "paper_ids": [
    "2019-data-validation-for-ml"
  ],
  "paper_sections": [
    "Section4: detecting training/serving skew with dataset statistics"
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
  "entrypoint": "solution.categorical_skew",
  "physical_contract": {
    "frames": [],
    "units": {
      "counts": "nonnegative observation counts",
      "probability": "dimensionless frequency",
      "threshold": "dimensionless maximum absolute probability difference"
    },
    "axes": "Categories are explicitly named operating conditions, not physical vector axes.",
    "timestamp_assumptions": "One aligned training/serving slice; callers choose comparable collection windows.",
    "batching": "Two count histograms for one feature and one slice."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-12,
    "atol": 1e-12,
    "public_case_families": [
      "same counts at different scale",
      "new category with shifted frequencies"
    ],
    "hidden_case_families": [
      "zero-count categories",
      "empty/zero totals",
      "strict threshold equality",
      "large integer counts",
      "invalid names/types",
      "nonmutation"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "457c5db60677454e682268120ccda2c720a6fc443f094b013b715f9c9bb36b4c"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:457c5db60677454e682268120ccda2c720a6fc443f094b013b715f9c9bb36b4c",
    "evaluator_sha256": "457c5db60677454e682268120ccda2c720a6fc443f094b013b715f9c9bb36b4c",
    "generated_fixture_hash": "457c5db60677454e682268120ccda2c720a6fc443f094b013b715f9c9bb36b4c"
  },
  "provenance": {
    "authoring_notes": "The paper motivates comparisons of dataset statistics. This aligned maximum-frequency-difference contract is an explicit teaching metric; its threshold is supplied and is not a statistical significance test or complete drift detector.",
    "primary_urls": [
      "https://research.google/pubs/data-validation-for-machine-learning/"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2019-data-validation-for-ml.md",
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

# Compare Training and Serving Distributions

## Learning objective

Compare aligned categorical frequencies while distinguishing distribution shift from dataset size.

## Source and scope

The paper motivates comparisons of dataset statistics. This aligned maximum-frequency-difference contract is an explicit teaching metric; its threshold is supplied and is not a statistical significance test or complete drift detector. Source location: Section4: detecting training/serving skew with dataset statistics. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate names/counts/totals, align the union, compute per-histogram frequencies and signed deltas, then the maximum distance. O(C log C) time and O(C) output space.

## Evaluator plan

Public cases: same counts at different scale; new category with shifted frequencies. Hidden cases: zero-count categories; empty/zero totals; strict threshold equality; large integer counts; invalid names/types; nonmutation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
