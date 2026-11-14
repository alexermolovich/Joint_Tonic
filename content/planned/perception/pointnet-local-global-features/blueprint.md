---
schema_version: 1
problem_id: pointnet-local-global-features
content_version: 0.1.0
status: reviewed
title: Concatenate Local and Global Features for Segmentation
summary: Concatenate Local and Global Features for Segmentation
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - perception
topics:
  - pointnet
  - paper-component
paper_ids:
  - 2017-pointnet
paper_sections:
  - Mechanism and scope defined in theory.md
track_ids: []
prerequisite_problem_ids:
  - pointnet-symmetric-pooling
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
entrypoint: solution.concat_local_global
physical_contract:
  frames:
    - Declared explicitly in learner contract
  units:
    features: dimensionless; image indices in pixels where applicable
  axes: 'local(B,N,D), global_features(B,G); output(B,N,D+G).'
  timestamp_assumptions: Same upstream observation or training snapshot; no timestamp input.
  batching: 'local(B,N,D), global_features(B,G); output(B,N,D+G).'
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
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original teaching contract and synthetic fixtures, no copied paper
    prose/figures/code.
  primary_urls:
    - 'https://arxiv.org/abs/1612.00593'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---

# Concatenate Local and Global Features for Segmentation

## Contract

Implement concat_local_global(local, global_features). Inputs are finite NumPy arrays of same dtype float32 or float64. local shape (B,N,D), global_features shape (B,G); 0<=B,N<=1024, 1<=D,G<=4096; every input and output at most1,000,000 elements. For each cloud b and point n return local[b,n,:] followed by global_features[b,:]. Preserve dtype, order, values and inputs; return independent storage. B=0 or N=0 returns correctly shaped empty output. Noncontiguous inputs supported. TypeError for non-array inputs; ValueError for all other violations including shape/dtype/limits/nonfinite data. Features are dimensionless learned coordinates, not XYZ; each cloud's local/global features describe the same upstream frame and observation. No pooling, MLP, masks, segmentation classifier, or coordinate registration is performed.

## Plan and proof

Implement only the typed component above. Independent review precedes publication. Validate both worked examples, documented errors and boundaries, stable layout/order, input preservation and realistic batches. Use actual isolated Run/Submit checks; no performance leaderboard. Source is the paired paper card and primary URL. Original theory contains defined mathematics and a static trace-table visual with text equivalent. Runtime image digest is pending; actual local worker caps are declared.
