---
schema_version: 1
problem_id: physical-ai-incident-triage
content_version: 0.1.0
status: reviewed
title: Triage a Physical-AI Deployment Incident
summary: >-
  Reduce a bounded event window into a deterministic operator queue without
  confusing duplicates, stale events or severity.
type: incident
difficulty: medium
estimated_minutes: 30
domains:
  - robotics-mlops
topics:
  - incident-analysis
  - robot-monitoring
paper_ids:
  - 2017-ml-test-score
paper_sections:
  - 'SectionV: Monitoring tests'
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
entrypoint: solution.triage_events
physical_contract:
  frames: []
  units:
    time: integer milliseconds on one synchronized run clock
    count: event records
  axes: 'Component IDs identify logging sources, not robot axes.'
  timestamp_assumptions: >-
    Include the closed window [now_ms-window_ms,now_ms]; negative cutoff is
    allowed.
  batching: One event snapshot; group retained records by component.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - severity and aggregation
    - closed-window cutoff
  hidden_case_families:
    - priority ties
    - duplicate records
    - empty window
    - future timestamps
    - invalid fields and bounds
    - immutable inputs
  performance_class: none; no timing leaderboard
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: mlops-batch2-draft-0.1.0
  evaluator_sha256: null
provenance:
  authoring_notes: >-
    The paper motivates monitored operational evidence. The event taxonomy,
    severity mapping and queue ordering are original educational policy; this
    function summarizes synthetic events and cannot stop, recover or approve a
    real robot.
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

# Triage a Physical-AI Deployment Incident

## Learning objective

Reduce a bounded event window into a deterministic operator queue without confusing duplicates, stale events or severity.

## Source and scope

The paper motivates monitored operational evidence. The event taxonomy, severity mapping and queue ordering are original educational policy; this function summarizes synthetic events and cannot stop, recover or approve a real robot. Source location: SectionV: Monitoring tests. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

One validated pass and one windowed reduction, then sort C component summaries. O(E+C log C) time, O(C) reduction storage plus validation.

## Evaluator plan

Public cases: severity and aggregation; closed-window cutoff. Hidden cases: priority ties; duplicate records; empty window; future timestamps; invalid fields and bounds; immutable inputs. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
