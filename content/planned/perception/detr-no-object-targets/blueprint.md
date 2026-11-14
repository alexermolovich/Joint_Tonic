---
schema_version: 1
problem_id: detr-no-object-targets
content_version: 0.1.0
status: reviewed
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
  image_status: pending-image-build
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
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

## Contract

Implement build_query_targets(labels, target_valid, matches, num_classes, eos_weight). labels and matches are NumPy int64 arrays; target_valid is NumPy bool. labels/target_valid shape(B,M), matches(B,Q),1<=B<=128,0<=M<=300,1<=Q<=300. num_classes is built-in int excluding bool in[1,1000]. All label entries including padding are in[0,num_classes). matches entries are -1 for unmatched or target indices[0,M); each nonnegative match must refer to a true target_valid slot and may appear at most once per batch. Valid targets need not all be matched. eos_weight is built-in int/float excluding bool in[0,1]. Return new int64 classes(B,Q), defaulting unmatched queries to num_classes (no-object), and float64 weights(B,Q), defaulting unmatched to eos_weight and matched to1. Preserve inputs; noncontiguous supported. TypeError for non-array arguments; ValueError for all other violations. This handles padded target sets and unmatched query supervision; it does not construct image-feature padding masks, solve assignment, or calculate cross-entropy. Indices/weights are dimensionless; each batch is one image exposure.

## Plan and verification

Review source fidelity, mathematics, numerical examples and edge/error behavior before implementation. Implement original starter/reference/public+hidden tests. Confirm actual isolated Run and Submit, and a starter negative control. Use static numerical/shape traces with text alternatives and original theory. Record only actual local worker caps; an OCI image digest remains pending. No dataset or full-paper reproduction is implied.
