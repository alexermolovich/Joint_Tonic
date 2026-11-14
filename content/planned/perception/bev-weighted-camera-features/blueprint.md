---
schema_version: 1
problem_id: bev-weighted-camera-features
content_version: 0.1.0
status: reviewed
title: Aggregate Multi-Camera Features with Attention Weights
summary: Aggregate Multi-Camera Features with Attention Weights
type: function
difficulty: easy
estimated_minutes: 30
domains:
  - perception
topics:
  - bevformer
  - paper-component
paper_ids:
  - 2022-bevformer
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
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
entrypoint: solution.aggregate_camera_features
physical_contract:
  frames:
    - Contract declares observation and coordinate assumptions
  units:
    features: dimensionless; ray distances in meters where applicable
  axes: >-
    features(B,Q,C,S,D),weights(B,Q,C,S),valid(B,Q,C,S);
    output(B,Q,D),observed(B,Q).
  timestamp_assumptions: One synchronized upstream observation or training snapshot.
  batching: >-
    features(B,Q,C,S,D),weights(B,Q,C,S),valid(B,Q,C,S);
    output(B,Q,D),observed(B,Q).
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
    - 'https://arxiv.org/abs/2203.17270'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---

# Aggregate Multi-Camera Features with Attention Weights

## Contract

Implement aggregate_camera_features(features, weights, valid). features and weights are finite NumPy float64, shapes(B,Q,C,S,D) and(B,Q,C,S); valid is NumPy bool same shape as weights. 1<=B,Q,C,S,D<=128; features at most1,000,000 elements; abs feature values<=1e6; weights in[0,1e6]. Set invalid contribution weights to zero, sum remaining weights over camera and sample axes, and return their weighted mean feature per (B,Q). Where total valid weight is zero return an all-zero feature and observed=False; otherwise observed=True. Return new float64 output(B,Q,D) and bool observed(B,Q); preserve inputs and support noncontiguous arrays. Validate all feature/weight entries including invalid slots. TypeError for non-arrays; ValueError for other violations. Features are dimensionless and already sampled at projections of one ego-frame BEV query from synchronized calibrated images; camera index is not a spatial axis. This is an explicitly simplified global weighted reduction, not BEVFormer's full per-camera/head deformable-attention normalization, learned offsets, bilinear sampling, or temporal fusion.

## Plan and verification

Review source fidelity, mathematics, numerical examples and edge/error behavior before implementation. Implement original starter/reference/public+hidden tests. Confirm actual isolated Run and Submit, and a starter negative control. Use static numerical/shape traces with text alternatives and original theory. Record only actual local worker caps; an OCI image digest remains pending. No dataset or full-paper reproduction is implied.
