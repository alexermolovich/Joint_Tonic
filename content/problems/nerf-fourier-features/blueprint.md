---
schema_version: 1
problem_id: nerf-fourier-features
content_version: 1.0.0
status: implemented
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
  evaluator_sha256: c383ca3fc49fc1f49399f0def6f938bd7aa8220f9d827b94b61f733de50f34b6
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

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/nerf-fourier-features. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Construct increasing frequencies 2^ell*pi. Multiplying positions with a separate level axis produces N×L×3 phases. Concatenate sine and cosine along the last axis and flatten the last two axes, yielding level-major channel order. Explicit dimensions preserve N=0 and L=0. Complexity and storage are O(NL). Small roundoff near trigonometric zeros is expected.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox nerf-fourier-features. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
