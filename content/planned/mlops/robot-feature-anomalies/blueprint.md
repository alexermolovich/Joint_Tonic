---
{
  "schema_version": 1,
  "problem_id": "robot-feature-anomalies",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Detect Missing, Range, Domain, and Shape Anomalies",
  "summary": "Return located schema violations from robot feature records without treating malformed data as valid zero values.",
  "type": "function",
  "difficulty": "hard",
  "estimated_minutes": 45,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "data-validation",
    "schema-anomalies"
  ],
  "paper_ids": [
    "2019-data-validation-for-ml"
  ],
  "paper_sections": [
    "Section3: schema-based validation and actionable anomalies"
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
    "budget_status": "actual shared worker limits; this draft has not run"
  },
  "entrypoint": "solution.feature_anomalies",
  "physical_contract": {
    "frames": [
      "Fixed upstream frame per named feature"
    ],
    "units": {
      "numeric": "Schema bounds use the feature's unchanged upstream physical unit",
      "category": "dimensionless labels"
    },
    "axes": "Each record is one aligned observation; array axes are the schema's declared feature shape.",
    "timestamp_assumptions": "Alignment/calibration is upstream; this function sees ordered observation records, not timestamps.",
    "batching": "At most1000 records; each feature has a separately declared shape and kind."
  },
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "missing and numeric range",
      "category and shape priority"
    ],
    "hidden_case_families": [
      "optional fields",
      "unexpected fields",
      "nonfinite priority",
      "scalar shapes",
      "invalid schemas",
      "bounded array payloads",
      "deterministic output"
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
    "authoring_notes": "The source motivates schema validation and located anomalies. This small numeric/categorical schema is original and complements the existing full episode validator; it does not infer a schema, convert physical units or implement every production validation rule.",
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

# Detect Missing, Range, Domain, and Shape Anomalies

## Learning objective

Return located schema violations from robot feature records without treating malformed data as valid zero values.

## Source and scope

The source motivates schema validation and located anomalies. This small numeric/categorical schema is original and complements the existing full episode validator; it does not infer a schema, convert physical units or implement every production validation rule. Source location: Section3: schema-based validation and actionable anomalies. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate bounded schema and workload, then inspect record/name union with ordered checks. O(total scalar entries+issue count log issue count) plus bounded feature lookups; no data coercion.

## Evaluator plan

Public cases: missing and numeric range; category and shape priority. Hidden cases: optional fields; unexpected fields; nonfinite priority; scalar shapes; invalid schemas; bounded array payloads; deterministic output. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
