---
schema_version: 1
problem_id: vit-patchify-reconstruct
content_version: 1.0.0
status: implemented
title: Patchify and Reconstruct an Image Tensor
summary: >-
  Convert channels-first images into ordered patch vectors and reconstruct every
  input pixel.
type: function
difficulty: easy
estimated_minutes: 30
domains:
  - perception
topics:
  - vision-transformer
  - image-layout
  - patch-tokens
paper_ids:
  - 2021-vision-transformer
paper_sections:
  - 'Section 3.1: Vision Transformer, image patches before linear projection'
track_ids: []
prerequisite_problem_ids: []
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
entrypoint: solution.patchify
physical_contract:
  frames:
    - image pixel lattice
  units:
    values: unchanged input intensity units
    patch_size: pixels
  axes: >-
    B,C,H,W input; H increases down, W right; patches row-major; elements
    channel then local row then local column.
  timestamp_assumptions: >-
    No timestamp input; any temporal or scene alignment is an upstream caller
    responsibility.
  batching: >-
    0<=B<=1024 independent images; 1<=C,H,W,P<=4096 with divisibility. No
    temporal dimension, resize, crop, or padding.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - rectangular two-patch image
    - multichannel patch order
    - P=1 identity layout
  hidden_case_families:
    - zero batch and rectangular grids
    - noncontiguous arrays
    - bad divisibility and mismatched image shape
    - input and output memory independence
  performance_class: none
  evaluator_sha256: afa4bc0571f6805cadc787c41c0e1636fa7e4fe4a634fe863b8f0ab557485428
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
    - 'https://arxiv.org/abs/2010.11929'
  implementation_urls: []
owners:
  - ui_issue_scout
reviewers:
  - paper_explanations
---
# Patchify and Reconstruct an Image Tensor

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/vit-patchify-reconstruct. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate the explicit image shape and patch size, then separate H and W into grid and within-patch axes. Transpose B,C,gridH,P,gridW,P to B,gridH,gridW,C,P,P before flattening. The inverse transposes those axes back. A final copy guarantees independent storage even for P=1 or a single patch. Both operations take O(BCHW) time and output memory; no pixel arithmetic is needed.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox vit-patchify-reconstruct. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
