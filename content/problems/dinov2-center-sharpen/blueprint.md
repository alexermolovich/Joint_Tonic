---
schema_version: 1
problem_id: dinov2-center-sharpen
content_version: 1.0.0
status: implemented
title: Center and Sharpen Teacher Probabilities
summary: Center and Sharpen Teacher Probabilities
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - perception
topics:
  - dinov2
  - paper-component
paper_ids:
  - 2023-dinov2
paper_sections:
  - Mechanism and scope defined in theory.md
track_ids: []
prerequisite_problem_ids: []
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
entrypoint: solution.center_sharpen
physical_contract:
  frames:
    - Declared explicitly in learner contract
  units:
    features: dimensionless; image indices in pixels where applicable
  axes: 'logits(B,K), center(K,), temperature scalar; probabilities(B,K).'
  timestamp_assumptions: Same upstream observation or training snapshot; no timestamp input.
  batching: 'logits(B,K), center(K,), temperature scalar; probabilities(B,K).'
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
    - deterministic-order
    - realistic-batch
  performance_class: none
  evaluator_sha256: 1d81100e31916aff421dd7b5633c6a094318811cb91bf895c818e7dcce70e9d3
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original teaching contract and synthetic fixtures, no copied paper
    prose/figures/code.
  primary_urls:
    - 'https://arxiv.org/abs/2304.07193'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Center and Sharpen Teacher Probabilities

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/dinov2-center-sharpen. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Subtract the supplied center and divide by positive temperature. Subtract each row's maximum, exponentiate, and normalize each row by its own sum. At least one exponent per row is one, preventing a zero denominator even for large score gaps. Complexity is O(BK) time and storage. This neither updates the center nor performs Sinkhorn balancing; those are distinct training operations.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox dinov2-center-sharpen. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
