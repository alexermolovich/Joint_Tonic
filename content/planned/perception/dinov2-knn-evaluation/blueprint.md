---
schema_version: 1
problem_id: dinov2-knn-evaluation
content_version: 0.1.0
status: reviewed
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
  image_status: pending-image-build
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
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

## Contract

Implement knn_classify(train, labels, queries, k, num_classes, temperature). train and queries are finite NumPy float64, shapes (M,D),(N,D), 1<=M<=512,0<=N<=512,1<=D<=256. Every feature row has L2 norm1 within atol1e-6,rtol0. labels is NumPy int64 (M,), in [0,num_classes). k and num_classes are built-in ints excluding bool;1<=k<=M,1<=num_classes<=1000. temperature is built-in int/float excluding bool in [1e-4,1e4]. Compute cosine dot products, choose k largest similarities per query with lower training index breaking ties, apply stable softmax over selected similarities divided by temperature, and sum normalized neighbor weights by class. Return new int64 predictions(N,) using lowest class index on tied class scores, and float64 scores(N,num_classes). Empty queries allowed; inputs unchanged, noncontiguous supported. TypeError for any non-array among first3; ValueError for all other violations. Features are dimensionless frozen representations; no fitting, self-exclusion, row normalization, or accuracy calculation. A query may also be in train; it is not silently removed. Normalizing votes is a teaching convention that preserves the usual weighted-kNN ranking.

## Plan and verification

Review source fidelity, mathematics, numerical examples and edge/error behavior before implementation. Implement original starter/reference/public+hidden tests. Confirm actual isolated Run and Submit, and a starter negative control. Use static numerical/shape traces with text alternatives and original theory. Record only actual local worker caps; an OCI image digest remains pending. No dataset or full-paper reproduction is implied.
