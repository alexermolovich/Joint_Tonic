---
schema_version: 1
problem_id: robot-ml-readiness-score
content_version: 0.1.0
status: reviewed
title: Score a Robot ML System for Production Readiness
summary: >-
  Aggregate documented manual and automated checks without letting strong
  categories conceal missing ones.
type: function
difficulty: easy
estimated_minutes: 20
domains:
  - robotics-mlops
topics:
  - production-readiness
  - test-evidence
paper_ids:
  - 2017-ml-test-score
paper_sections:
  - 'SectionVI.A: Computing an ML Test Score'
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
entrypoint: solution.readiness_score
physical_contract:
  frames: []
  units:
    score: dimensionless rubric points
  axes: >-
    Four fixed readiness categories; list positions are distinct declared
    checks.
  timestamp_assumptions: One already-curated evidence snapshot; no freshness inference.
  batching: One system score per call.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - unequal category coverage
    - all categories empty
  hidden_case_families:
    - all automated
    - manual-only categories
    - invalid statuses/keys
    - seven-item category bound
    - nonmutation
  performance_class: none; no timing leaderboard
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: mlops-batch2-draft-0.1.0
  evaluator_sha256: null
provenance:
  authoring_notes: >-
    The half-point/manual, full-point/automated and minimum-category aggregation
    follows the paper. Supplied check lists and robot examples are original;
    this function does not reproduce the paper's full28-check questionnaire or
    certify operational safety.
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

# Score a Robot ML System for Production Readiness

## Learning objective

Aggregate documented manual and automated checks without letting strong categories conceal missing ones.

## Source and scope

The half-point/manual, full-point/automated and minimum-category aggregation follows the paper. Supplied check lists and robot examples are original; this function does not reproduce the paper's full28-check questionnaire or certify operational safety. Source location: SectionVI.A: Computing an ML Test Score. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate exact category keys and each list/status, then sum fixed credits and take the minimum. At most28 supplied statuses; constant bounded memory.

## Evaluator plan

Public cases: unequal category coverage; all categories empty. Hidden cases: all automated; manual-only categories; invalid statuses/keys; seven-item category bound; nonmutation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
