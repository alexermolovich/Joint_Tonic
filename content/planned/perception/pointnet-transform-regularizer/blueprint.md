---
schema_version: 1
problem_id: pointnet-transform-regularizer
content_version: 0.1.0
status: reviewed
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
  image_status: pending-image-build
  dependencies:
    torch: 2.6.0+cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
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

## Contract

Implement feature_transform_penalty(transforms). Input is a finite CPU PyTorch tensor float32 or float64, shape (B,D,D), 1<=B<=256, 1<=D<=64, at most1,000,000 elements, abs values<=10. Return a scalar tensor of the same dtype/device equal to the batch mean of squared Frobenius norms ||A A.T-I||_F^2. Sum over both matrix axes and average only over B. Preserve gradients, inputs and new output storage. TypeError for non-tensor; ValueError for other violations. Empty batches rejected. This penalizes deviation from orthogonality; it does not enforce determinant+1. Feature coordinates are dimensionless, not necessarily a physical rotation. No T-Net, optimizer, classifier, or full PointNet training.

## Plan and verification

Review source fidelity, mathematics, numerical examples and edge/error behavior before implementation. Implement original starter/reference/public+hidden tests. Confirm actual isolated Run and Submit, and a starter negative control. Use static numerical/shape traces with text alternatives and original theory. Record only actual local worker caps; an OCI image digest remains pending. No dataset or full-paper reproduction is implied.
