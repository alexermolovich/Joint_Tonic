---
schema_version: 1
problem_id: pointnet-transform-regularizer
content_version: 1.0.0
status: implemented
title: Regularize a Learned Feature Transform
summary: Regularize a Learned Feature Transform
type: function
difficulty: easy
estimated_minutes: 30
domains:
  - perception
topics:
  - pointnet
  - paper-component
paper_ids:
  - 2017-pointnet
paper_sections:
  - Mechanism and limits stated in theory.md
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  dependencies:
    torch: 2.6.0+cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.feature_transform_penalty
physical_contract:
  frames:
    - Contract declares observation and coordinate assumptions
  units:
    features: dimensionless; ray distances in meters where applicable
  axes: 'transforms(B,D,D); scalar loss, B,D>=1.'
  timestamp_assumptions: One synchronized upstream observation or training snapshot.
  batching: 'transforms(B,D,D); scalar loss, B,D>=1.'
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
  evaluator_sha256: 53d8593b15a813ad3725aaf37f677df2942925e1e6577b07b1bf0007bdbd5d96
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original scoped exercise; no paper figure/prose/code copied.
  primary_urls:
    - 'https://arxiv.org/abs/1612.00593'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Regularize a Learned Feature Transform

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/pointnet-transform-regularizer. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Compute A @ A.transpose(-1,-2), subtract a D×D identity, square and sum over both matrix axes, then average over B. The reduction order defines the loss scale. Keep autograd connected. Reflections have zero penalty too, so this is feature orthogonality regularization rather than a constraint to proper spatial rotations. Time is O(BD³), temporary storage O(BD²).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox pointnet-transform-regularizer. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
