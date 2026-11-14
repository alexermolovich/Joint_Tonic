---
schema_version: 1
problem_id: nerf-stratified-samples
content_version: 1.0.0
status: implemented
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
  evaluator_sha256: 39d7e3f84727ae596c3f8444a58f962c6cad150716439a4e37589a0db92da7c8
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

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/nerf-stratified-samples. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Compute one interval width (far-near)/S per ray, add the supplied unit draws to increasing bin indices, multiply by width and shift by near. The result is ordered by construction; no sorting or RNG is needed. Use explicit ray and sample axes to avoid sharing one ray's bounds with another. Time and output storage are O(RS).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox nerf-stratified-samples. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
