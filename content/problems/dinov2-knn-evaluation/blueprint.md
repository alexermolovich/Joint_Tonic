---
schema_version: 1
problem_id: dinov2-knn-evaluation
content_version: 1.0.0
status: implemented
title: Evaluate Frozen Features with k-NN
summary: Evaluate Frozen Features with k-NN
type: function
difficulty: medium
estimated_minutes: 30
domains:
  - perception
topics:
  - dinov2
  - paper-component
paper_ids:
  - 2023-dinov2
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
entrypoint: solution.knn_classify
physical_contract:
  frames:
    - Contract declares observation and coordinate assumptions
  units:
    features: dimensionless; ray distances in meters where applicable
  axes: 'train(M,D),labels(M,),queries(N,D); predictions(N,), class_scores(N,C).'
  timestamp_assumptions: One synchronized upstream observation or training snapshot.
  batching: 'train(M,D),labels(M,),queries(N,D); predictions(N,), class_scores(N,C).'
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
  evaluator_sha256: 0e3ca4fb13523ef11dc3be13e674d0ff283b5e9b58ae2d18fc270a72bfa4bf9b
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original scoped exercise; no paper figure/prose/code copied.
  primary_urls:
    - 'https://arxiv.org/abs/2304.07193'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Evaluate Frozen Features with k-NN

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/dinov2-knn-evaluation. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Form query-by-training cosine scores, stable-sort neighbors, and retain the first k. Apply a stable softmax only within each selected neighborhood, then accumulate weights by training label. Argmax selects the lowest class index on exact ties. Empty query batches retain the class dimension. Feature extraction, split design and accuracy computation remain outside this function. Similarity costs O(NMD), neighbor sorting O(NM log M).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox dinov2-knn-evaluation. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
