---
schema_version: 1
problem_id: nerf-stratified-samples
content_version: 0.1.0
status: reviewed
title: Stratify Samples Along Near and Far Bounds
summary: Stratify Samples Along Near and Far Bounds
type: function
difficulty: easy
estimated_minutes: 30
domains:
  - perception
topics:
  - nerf
  - paper-component
paper_ids:
  - 2020-nerf
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
entrypoint: solution.stratified_samples
physical_contract:
  frames:
    - Contract declares observation and coordinate assumptions
  units:
    features: dimensionless; ray distances in meters where applicable
  axes: 'near(R,),far(R,),draws(R,S); output(R,S).'
  timestamp_assumptions: One synchronized upstream observation or training snapshot.
  batching: 'near(R,),far(R,),draws(R,S); output(R,S).'
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
    - 'https://arxiv.org/abs/2003.08934'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---

# Stratify Samples Along Near and Far Bounds

## Contract

Implement stratified_samples(near, far, draws). All inputs are finite NumPy float64 arrays. near and far have shape (R,), 1<=R<=4096, satisfying 0<=near<far<=1e6 meters and far-near>=1e-6 m. draws has shape (R,S), 1<=S<=1024, at most1,000,000 elements, with values in [0,1). Divide each [near,far] into S equal-width bins; sample one depth per bin with the corresponding supplied draw. z[r,i]=near[r]+(i+draws[r,i])*(far[r]-near[r])/S. Return new float64 (R,S); no RNG calls, mutation or sorting. Noncontiguous arrays supported. TypeError for non-array inputs; ValueError for all other violations. Ray directions are already normalized, so z is meters along each ray, not camera optical z. One static scene exposure; no inverse-depth spacing, hierarchical PDF sampling, or appended infinity. Equal-width full-interval bins are the explicit teaching discretization, not every implementation's endpoint-midpoint convention.

## Plan and verification

Review source fidelity, mathematics, numerical examples and edge/error behavior before implementation. Implement original starter/reference/public+hidden tests. Confirm actual isolated Run and Submit, and a starter negative control. Use static numerical/shape traces with text alternatives and original theory. Record only actual local worker caps; an OCI image digest remains pending. No dataset or full-paper reproduction is implied.
