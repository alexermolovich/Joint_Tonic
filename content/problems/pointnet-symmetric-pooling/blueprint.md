---
schema_version: 1
problem_id: pointnet-symmetric-pooling
content_version: 1.0.0
status: implemented
title: Prove Permutation Invariance with Symmetric Pooling
summary: >-
  Pool valid point features channel by channel and demonstrate that point order
  cannot change the result.
type: function
difficulty: easy
estimated_minutes: 30
domains:
  - perception
topics:
  - point-clouds
  - permutation-invariance
  - masked-pooling
paper_ids:
  - 2017-pointnet
paper_sections:
  - 'Section 4.2: symmetry function for unordered input'
track_ids: []
prerequisite_problem_ids:
  - se3-transform-points
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
entrypoint: solution.symmetric_point_pool
physical_contract:
  frames:
    - features derived from one consistently calibrated point-cloud frame
  units:
    features: dimensionless learned features
  axes: 'B cloud batch, N unordered point slots, D feature channels; reduce only N.'
  timestamp_assumptions: >-
    No timestamp input; any temporal or scene alignment is an upstream caller
    responsibility.
  batching: >-
    B,N,D positive. A boolean B-by-N mask marks valid point slots; every cloud
    has at least one valid point.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - permutation with channel maxima at different points
    - negative valid features with high padding
    - one valid point
  hidden_case_families:
    - different masks per cloud
    - duplicate features and tied maxima
    - all-invalid cloud and empty dimensions rejected
    - permutations applied jointly to mask and features
    - noncontiguous inputs and independent output
  performance_class: none
  evaluator_sha256: 54ba62d5ab20e8e8cf73940ea6332335ed902112845e30c1a1f194216d113b35
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
    - 'https://arxiv.org/abs/1612.00593'
  implementation_urls: []
owners:
  - ui_issue_scout
reviewers:
  - paper_explanations
---
# Prove Permutation Invariance with Symmetric Pooling

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/pointnet-symmetric-pooling. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate all values, including padding, and require at least one valid point per cloud. Replace invalid slots with negative infinity for the reduction only, then take a maximum along N. Every channel can choose a different winning point. Max is unchanged by reordering its operands, so a joint feature/mask permutation leaves the output invariant. Cost is O(BND) time and up to O(BND) temporary storage.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox pointnet-symmetric-pooling. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
