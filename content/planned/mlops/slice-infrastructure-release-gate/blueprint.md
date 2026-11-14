---
schema_version: 1
problem_id: slice-infrastructure-release-gate
content_version: 0.1.0
status: reviewed
title: Gate a Release on Slice and Infrastructure Tests
summary: >-
  Reject a candidate when any required scenario or infrastructure check lacks
  current passing evidence.
type: function
difficulty: medium
estimated_minutes: 30
domains:
  - robotics-mlops
topics:
  - release-gates
  - versioned-evidence
paper_ids:
  - 2017-ml-test-score
paper_sections:
  - 'Model6: important data slices; Infrastructure tests; SectionV monitoring'
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: python
  python: 3.12.3
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  image_digest: null
  image_status: pending OCI build; baseline worker exists
  dependencies: {}
  platform: linux-x86_64-cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  budget_status: actual shared worker limits; this draft has not run
entrypoint: solution.release_rejections
physical_contract:
  frames: []
  units:
    time: integer milliseconds on one synchronized monotonic run clock
  axes: Check IDs are namespaced slice/name or infra/name; no spatial axes.
  timestamp_assumptions: >-
    Evidence completion and now share a clock; future evidence is rejected as a
    reason.
  batching: One candidate and required-check set per call.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - mixed evidence reasons
    - inclusive freshness boundary
  hidden_case_families:
    - reason priority
    - duplicate requirements
    - extra valid evidence
    - empty requirements
    - malformed records
    - large timestamps
  performance_class: none; no timing leaderboard
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: mlops-batch2-draft-0.1.0
  evaluator_sha256: null
provenance:
  authoring_notes: >-
    The source motivates testing important slices and ML infrastructure. Version
    matching, freshness thresholds, reason priority and ID format are original
    teaching policies; this is an evidence gate, not a complete safety
    authorization.
  primary_urls:
    - >-
      https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
  implementation_urls: []
  paper_card: research/papers/mlops-sim2real/2017-ml-test-score.md
  manifest: research/manifests/mlops-sim2real.md
owners:
  - code_issue_scout
reviewers:
  - perception_implementation
---

# Gate a Release on Slice and Infrastructure Tests

## Learning objective

Reject a candidate when any required scenario or infrastructure check lacks current passing evidence.

## Source and scope

The source motivates testing important slices and ML infrastructure. Version matching, freshness thresholds, reason priority and ID format are original teaching policies; this is an evidence gate, not a complete safety authorization. Source location: Model6: important data slices; Infrastructure tests; SectionV monitoring. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate metadata and bounds; iterate sorted unique requirements, selecting the first rejection condition. O(R log R+E) time and O(R+E) validation/output memory.

## Evaluator plan

Public cases: mixed evidence reasons; inclusive freshness boundary. Hidden cases: reason priority; duplicate requirements; extra valid evidence; empty requirements; malformed records; large timestamps. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
