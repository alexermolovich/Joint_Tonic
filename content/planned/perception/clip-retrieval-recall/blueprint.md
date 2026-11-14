---
schema_version: 1
problem_id: clip-retrieval-recall
content_version: 0.1.0
status: reviewed
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
  image_status: pending-image-build
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
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

## Contract

Implement retrieval_recall(scores, k). scores is a finite NumPy float64 array (N,N), 1<=N<=2048, absolute entries <=1e6. Row i is image i; column j is text j. The only positive for image i is text i and vice versa. k is a built-in Python int excluding bool with 1<=k<=N. Rank by descending score and break equal scores by lower candidate index. Return exactly {'image_to_text': float, 'text_to_image': float}, fractions of queries whose paired item ranks within k. For image-to-text rank each row; for text-to-image rank each column. Preserve scores. Noncontiguous arrays supported. TypeError for non-array scores; ValueError for all other violations. Empty collections are rejected; k=N gives both recalls1. Scores are dimensionless, not probabilities; no timestamps or robot frames. This exercise computes single-positive recall, not image encoder inference, multi-positive retrieval, average precision, or confidence intervals.

## Plan and proof

Implement only the typed component above. Independent review precedes publication. Validate both worked examples, documented errors and boundaries, stable layout/order, input preservation and realistic batches. Use actual isolated Run/Submit checks; no performance leaderboard. Source is the paired paper card and primary URL. Original theory contains defined mathematics and a static trace-table visual with text equivalent. Runtime image digest is pending; actual local worker caps are declared.
