---
schema_version: 1
problem_id: clip-retrieval-recall
content_version: 1.0.0
status: implemented
title: Evaluate Cross-Modal Retrieval Recall at K
summary: Evaluate Cross-Modal Retrieval Recall at K
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - perception
topics:
  - clip
  - paper-component
paper_ids:
  - 2021-clip
paper_sections:
  - Mechanism and scope defined in theory.md
track_ids: []
prerequisite_problem_ids:
  - clip-normalize-embeddings
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
entrypoint: solution.retrieval_recall
physical_contract:
  frames:
    - Declared explicitly in learner contract
  units:
    features: dimensionless; image indices in pixels where applicable
  axes: 'scores(N,N), one paired collection; result dictionary of two scalar recalls.'
  timestamp_assumptions: Same upstream observation or training snapshot; no timestamp input.
  batching: 'scores(N,N), one paired collection; result dictionary of two scalar recalls.'
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
  evaluator_sha256: 42122fefa2bc259300020adaba382c7338833cab48456d2a49ca9b93f7fc4e00
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original teaching contract and synthetic fixtures, no copied paper
    prose/figures/code.
  primary_urls:
    - 'https://arxiv.org/abs/2103.00020'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Evaluate Cross-Modal Retrieval Recall at K

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/clip-retrieval-recall. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Use stable descending sorting along rows for image queries and columns for text queries. Original candidate order gives the lower-index tie rule. For each query test whether its diagonal positive appears in the first k indices, then average those Boolean hits. The two means are separate because ranking across the two axes can differ. Sorting costs O(N² log N) time and O(N²) space. No softmax or score calibration is needed.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox clip-retrieval-recall. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
