---
schema_version: 1
problem_id: vit-position-interpolation
content_version: 1.0.0
status: implemented
title: Interpolate 2D Positional Embeddings
summary: Interpolate 2D Positional Embeddings
type: function
difficulty: medium
estimated_minutes: 35
domains:
  - perception
topics:
  - vision-transformer
  - paper-component
paper_ids:
  - 2021-vision-transformer
paper_sections:
  - Mechanism and conventions defined in theory.md
track_ids: []
prerequisite_problem_ids:
  - vit-patch-class-tokens
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  dependencies:
    torch: 2.6.0+cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.resize_positions
physical_contract:
  frames:
    - Explicit caller-observation conventions in statement
  units:
    features: dimensionless
  axes: >-
    positions(1,1+H0*W0,D), old_grid(H0,W0),new_grid(H1,W1);
    result(1,1+H1*W1,D).
  timestamp_assumptions: One observation batch; no internal clock.
  batching: >-
    positions(1,1+H0*W0,D), old_grid(H0,W0),new_grid(H1,W1);
    result(1,1+H1*W1,D).
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - worked-examples
    - minimal-shape
  hidden_case_families:
    - validation
    - edge-policy
    - layout
    - preservation
    - independent-oracle
    - scale
  performance_class: cpu
  evaluator_sha256: 21ce99355a0364ff67b13857b1d95fde9e45f3258d026e4be05479742968e4da
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original bounded teaching task. No copied source code or figure.
  primary_urls:
    - 'https://arxiv.org/abs/2010.11929'
  implementation_urls: []
  paper_card: research/papers/vision-vlm-3d/2021-vision-transformer.md
  manifest: research/manifests/vision-vlm-3d.md
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Interpolate 2D Positional Embeddings

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/vit-position-interpolation. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Separate the class row, reshape patch positions from the row-major sequence into H0×W0×D, and permute to channels-first format. Apply the pinned bicubic interpolation with align_corners=False and antialias=False, restore row-major sequence order, and concatenate the unchanged class row. Concatenation allocates independent storage and keeps both branches connected to autograd. Work is linear in D times the input and output spatial sizes.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox vit-position-interpolation. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
