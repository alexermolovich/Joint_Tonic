---
schema_version: 1
problem_id: detr-no-object-targets
content_version: 1.0.0
status: implemented
title: Handle the No-Object Class and Padding Masks
summary: Handle the No-Object Class and Padding Masks
type: function
difficulty: medium
estimated_minutes: 30
domains:
  - perception
topics:
  - detr
  - paper-component
paper_ids:
  - 2020-detr
paper_sections:
  - Mechanism and limits stated in theory.md
track_ids: []
prerequisite_problem_ids:
  - detr-matching-cost
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.build_query_targets
physical_contract:
  frames:
    - Contract declares observation and coordinate assumptions
  units:
    features: dimensionless; ray distances in meters where applicable
  axes: >-
    labels(B,M),target_valid(B,M),matches(B,Q); return
    classes(B,Q),weights(B,Q).
  timestamp_assumptions: One synchronized upstream observation or training snapshot.
  batching: >-
    labels(B,M),target_valid(B,M),matches(B,Q); return
    classes(B,Q),weights(B,Q).
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.e-7
  atol: 1.e-9
  public_case_families:
    - worked-examples
    - minimal-shape
  hidden_case_families:
    - validation
    - empty-policy
    - noncontiguous
    - immutability
    - numerical-boundaries
    - independent-oracle
  performance_class: none
  evaluator_sha256: e6639fcb3acff3b2278c44648b7086eb9abe0c07ab563be6147ae4e1569e42b9
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original scoped exercise; no paper figure/prose/code copied.
  primary_urls:
    - 'https://arxiv.org/abs/2005.12872'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Handle the No-Object Class and Padding Masks

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/detr-no-object-targets. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate the complete padded target set and every supplied assignment. Reject references to invalid slots and duplicate use of a target in the same image. Initialize query classes to C and weights to eos_weight, then fill matched entries from the target labels with unit weight. The assignment itself is an input; no matching solver or loss reduction is hidden here. Time is O(B(M+Q log Q)) with per-row duplicate validation.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox detr-no-object-targets. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
