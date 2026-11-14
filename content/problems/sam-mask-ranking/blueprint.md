---
schema_version: 1
problem_id: sam-mask-ranking
content_version: 1.0.0
status: implemented
title: Rank Candidate Masks with Predicted IoU
summary: Rank Candidate Masks with Predicted IoU
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - perception
topics:
  - segment-anything
  - paper-component
paper_ids:
  - 2023-segment-anything
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
entrypoint: solution.rank_masks
physical_contract:
  frames:
    - Declared explicitly in learner contract
  units:
    features: dimensionless; image indices in pixels where applicable
  axes: >-
    masks(N,H,W), predicted_iou(N,), k; return selected(k,H,W), indices(k,),
    scores(k,).
  timestamp_assumptions: Same upstream observation or training snapshot; no timestamp input.
  batching: >-
    masks(N,H,W), predicted_iou(N,), k; return selected(k,H,W), indices(k,),
    scores(k,).
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
  evaluator_sha256: 2efe0afad619bfc6abe68b5e56481429e7f23c034dff832889b48d1089720603
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original teaching contract and synthetic fixtures, no copied paper
    prose/figures/code.
  primary_urls:
    - 'https://arxiv.org/abs/2304.02643'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Rank Candidate Masks with Predicted IoU

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/sam-mask-ranking. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Stable-sort descending raw quality scores and retain the first k original indices. Index masks and scores with the same indices and return independent arrays. No clipping, suppression, averaging, or mask conversion is performed. Sorting costs O(N log N), and copying selected masks costs O(kHW). Original indices preserve alignment with metadata outside this function.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox sam-mask-ranking. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
