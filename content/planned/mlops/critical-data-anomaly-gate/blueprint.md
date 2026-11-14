---
{
  "schema_version": 1,
  "problem_id": "critical-data-anomaly-gate",
  "content_version": "0.1.0",
  "status": "reviewed",
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
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "mlops-batch3-draft-0.1.0",
    "evaluator_sha256": null
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
  "reviewers": ["perception_implementation"]
}
---

# Block a Pipeline on Critical Data Anomalies

## Learning objective

Gate a pipeline using explicit anomaly severity and required-source coverage while retaining warnings for inspection.

## Source and scope

The paper motivates separating validation evidence from downstream pipeline execution. Required-source coverage, severity policy and conflict rules are original teaching choices; a passing data gate is not a robot safety guarantee. Source location: Data validation as a pipeline boundary; schema anomaly review. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate lists and tuple fields, build source sets and a severity map, derive sorted critical/warning/missing outputs. O(A+S+(A+S)log(A+S)) time including sorting; bounded metadata storage.

## Evaluator plan

Public cases: critical versus warning; missing validation source. Hidden cases: duplicate records; conflicting severities; extra checked source; empty required set; empty anomaly list; source consistency; input preservation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
