---
schema_version: 1
problem_id: dinov2-center-sharpen
content_version: 0.1.0
status: reviewed
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
  image_status: pending-image-build
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
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

## Contract

Implement center_sharpen(logits, center, temperature). logits and center are finite NumPy float64 arrays shaped (B,K) and (K,), with 1<=B,K<=1024, at most1,000,000 logits, and absolute values<=1e6. temperature is a built-in int/float excluding bool in [1e-4,1e4]. Compute row softmax((logits-center)/temperature) using a stable maximum subtraction. Return new float64 probabilities (B,K), preserving inputs and supporting noncontiguous arrays. Rows sum to1 within rtol1e-7,atol1e-9; underflow to0 is allowed. TypeError for non-array logits/center; ValueError for all other violations. No gradient contract (NumPy), center update, student loss, or Sinkhorn balancing. Coordinates are dimensionless prototype scores, not robot positions; center corresponds to the supplied training snapshot. This is the centering/sharpening variant discussed in the DINO family. DINOv2's improved training uses Sinkhorn-Knopp normalization; this component must not be presented as that full target-balancing procedure.

## Plan and proof

Implement only the typed component above. Independent review precedes publication. Validate both worked examples, documented errors and boundaries, stable layout/order, input preservation and realistic batches. Use actual isolated Run/Submit checks; no performance leaderboard. Source is the paired paper card and primary URL. Original theory contains defined mathematics and a static trace-table visual with text equivalent. Runtime image digest is pending; actual local worker caps are declared.
