---
schema_version: 1
problem_id: pointnet-local-global-features
content_version: 1.0.0
status: implemented
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
  evaluator_sha256: dd66bc704c046dae47523e1841544d90c3a44425379cecbe93551a23ce0aa4ea
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

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/pointnet-local-global-features. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Insert a singleton point axis into the B×G context, broadcast it to B×N×G, and concatenate after the local D channels. Concatenation allocates new storage and preserves empty batches/point sets. This is equivariant to point reordering: local rows move with their duplicated context. Cost and output memory are O(BN(D+G)); no reduction or learned parameters are introduced.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox pointnet-local-global-features. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
