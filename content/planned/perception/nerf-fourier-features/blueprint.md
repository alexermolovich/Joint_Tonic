---
schema_version: 1
problem_id: nerf-fourier-features
content_version: 0.1.0
status: reviewed
title: Encode 3D Positions with Fourier Features
summary: Encode 3D Positions with Fourier Features
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - perception
topics:
  - nerf
  - paper-component
paper_ids:
  - 2020-nerf
paper_sections:
  - Mechanism and scope defined in theory.md
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
entrypoint: solution.fourier_encode
physical_contract:
  frames:
    - Declared explicitly in learner contract
  units:
    features: dimensionless; image indices in pixels where applicable
  axes: 'positions(N,3), levels integer0..10; result(N,6*levels).'
  timestamp_assumptions: Same upstream observation or training snapshot; no timestamp input.
  batching: 'positions(N,3), levels integer0..10; result(N,6*levels).'
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
    - 'https://arxiv.org/abs/2003.08934'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---

# Encode 3D Positions with Fourier Features

## Contract

Implement fourier_encode(positions, levels). positions is finite NumPy float64 (N,3), 0<=N<=10000, absolute coordinates<=1e4. Coordinates are dimensionless normalized scene coordinates in one fixed frame; normalization from meters is upstream. levels is a built-in int excluding bool in [0,10]. Return a new float64 array (N,6*levels). For each level ell=0..levels-1, append the three sin(2**ell*pi*positions) coordinates followed by the three cos coordinates; concatenate levels in increasing order. Do not prepend raw coordinates, mix coordinate-major order, or divide by pi. Preserve inputs and support noncontiguous arrays. levels=0 returns (N,0); N=0 returns (0,6*levels). TypeError for non-array positions, ValueError for all remaining violations. Values compared rtol=1e-7,atol=1e-9. No timestamps, neural network, random Fourier matrix, or view-direction encoding.

## Plan and proof

Implement only the typed component above. Independent review precedes publication. Validate both worked examples, documented errors and boundaries, stable layout/order, input preservation and realistic batches. Use actual isolated Run/Submit checks; no performance leaderboard. Source is the paired paper card and primary URL. Original theory contains defined mathematics and a static trace-table visual with text equivalent. Runtime image digest is pending; actual local worker caps are declared.
