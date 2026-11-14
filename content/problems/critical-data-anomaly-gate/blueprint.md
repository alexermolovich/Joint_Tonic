---
{
  "schema_version": 1,
  "problem_id": "critical-data-anomaly-gate",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Block a Pipeline on Critical Data Anomalies",
  "summary": "Gate a pipeline using explicit anomaly severity and required-source coverage while retaining warnings for inspection.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "pipeline-gates",
    "data-quality"
  ],
  "paper_ids": [
    "2019-data-validation-for-ml"
  ],
  "paper_sections": [
    "Data validation as a pipeline boundary; schema anomaly review"
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
  "entrypoint": "solution.data_anomaly_gate",
  "physical_contract": {
    "frames": [],
    "units": {
      "ids": "dimensionless source and anomaly codes"
    },
    "axes": "Source IDs identify validated datasets or sensor streams.",
    "timestamp_assumptions": "A single versioned validation snapshot; freshness/version association is upstream.",
    "batching": "One pipeline snapshot with required sources, completed checks and anomaly records."
  },
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "critical versus warning",
      "missing validation source"
    ],
    "hidden_case_families": [
      "duplicate records",
      "conflicting severities",
      "extra checked source",
      "empty required set",
      "empty anomaly list",
      "source consistency",
      "input preservation"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "087fe57c681c02455aef07aabb6bd0eecf124159fffdf66649c721a4ef1b6483"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:087fe57c681c02455aef07aabb6bd0eecf124159fffdf66649c721a4ef1b6483",
    "evaluator_sha256": "087fe57c681c02455aef07aabb6bd0eecf124159fffdf66649c721a4ef1b6483",
    "generated_fixture_hash": "087fe57c681c02455aef07aabb6bd0eecf124159fffdf66649c721a4ef1b6483"
  },
  "provenance": {
    "authoring_notes": "The paper motivates separating validation evidence from downstream pipeline execution. Required-source coverage, severity policy and conflict rules are original teaching choices; a passing data gate is not a robot safety guarantee.",
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

# Block a Pipeline on Critical Data Anomalies

## Learning objective

Gate a pipeline using explicit anomaly severity and required-source coverage while retaining warnings for inspection.

## Source and scope

The paper motivates separating validation evidence from downstream pipeline execution. Required-source coverage, severity policy and conflict rules are original teaching choices; a passing data gate is not a robot safety guarantee. Source location: Data validation as a pipeline boundary; schema anomaly review. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate lists and tuple fields, build source sets and a severity map, derive sorted critical/warning/missing outputs. O(A+S+(A+S)log(A+S)) time including sorting; bounded metadata storage.

## Evaluator plan

Public cases: critical versus warning; missing validation source. Hidden cases: duplicate records; conflicting severities; extra checked source; empty required set; empty anomaly list; source consistency; input preservation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
