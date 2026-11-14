---
schema_version: 1
problem_id: nerf-alpha-compositing
content_version: 1.0.0
status: implemented
title: Compute Transmittance and Alpha Compositing Weights
summary: >-
  Turn ordered ray densities and metric interval lengths into sample visibility
  weights and remaining background mass.
type: function
difficulty: medium
estimated_minutes: 35
domains:
  - perception
topics:
  - neural-rendering
  - volume-rendering
  - visibility
paper_ids:
  - 2020-nerf
paper_sections:
  - >-
    Section 4: volume rendering with radiance fields, discrete rendering
    equation
track_ids: []
prerequisite_problem_ids:
  - project-camera-points
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  platform: linux-x86_64-cpu
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.alpha_compositing_weights
physical_contract:
  frames:
    - one scene frame per ray; unit ray direction assumed upstream
  units:
    density: inverse metres
    deltas: metres
    weights: dimensionless
    background: dimensionless
  axes: >-
    R independent rays, S intervals ordered near-to-far; no spatial coordinate
    axis in the supplied arrays.
  timestamp_assumptions: >-
    No timestamp input; any temporal or scene alignment is an upstream caller
    responsibility.
  batching: >-
    R,S positive; equal (R,S) arrays; last interval explicitly supplied; no
    padding or implicit infinite tail.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - two half-opaque intervals
    - different interval lengths
    - zero length and zero density
  hidden_case_families:
    - near-opaque front interval
    - tiny thickness stability
    - ray-independent batching
    - empty and invalid inputs
    - noncontiguous arrays and mass conservation
  performance_class: none
  evaluator_sha256: d19d710e6f24b654a583bc8dda554a703e5026205f19e45442f923267a5d306a
fixtures:
  source: >-
    original synthetic examples in examples.md; future generated fixtures use
    declared seed
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original bounded teaching contract and explanations; source mechanisms
    checked against the paired paper card and primary sources; no paper figures
    or implementation code copied.
  primary_urls:
    - 'https://arxiv.org/abs/2003.08934'
  implementation_urls: []
owners:
  - ui_issue_scout
reviewers:
  - paper_explanations
---
# Compute Transmittance and Alpha Compositing Weights

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/nerf-alpha-compositing. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Multiply density by metric length to get dimensionless optical thickness. Use -expm1(-q) for accurate opacity at tiny q. Construct exclusive cumulative thickness by prepending a zero column to the cumulative sum over all earlier intervals; avoid subtracting the current q from an inclusive sum, which loses small previous terms. Exponentiate its negative, multiply by opacity, and return exp(-sum(q)) for background. Do not renormalize or append an opaque last interval. Time and memory are O(RS).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox nerf-alpha-compositing. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
