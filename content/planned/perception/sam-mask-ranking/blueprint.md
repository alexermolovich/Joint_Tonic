---
schema_version: 1
problem_id: sam-mask-ranking
content_version: 0.1.0
status: reviewed
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
  image_status: pending-image-build
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
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

## Contract

Implement rank_masks(masks, predicted_iou, k). masks is a NumPy bool array (N,H,W), 0<=N<=1024, 1<=H,W<=512, at most1,000,000 elements. predicted_iou is finite NumPy float64 (N,), absolute values<=1e6. These are learned quality scores: preserve raw values, including values outside[0,1], rather than clipping or recalibrating. k is a built-in int excluding bool in [0,N]. Sort by decreasing score; ties choose lower original candidate index. Return (selected_masks, indices, selected_scores), new arrays of shapes (k,H,W),(k,),(k,) and dtype bool,int64,float64. Preserve inputs and support noncontiguous arrays. Empty candidates require k=0 and return correctly shaped empties. TypeError for non-array arguments; ValueError for all other violations. Masks share one image pixel frame with row down and column right; each candidate is an alternative interpretation of the same prompt and exposure. No mask averaging, overlap suppression, ground-truth IoU calculation, thresholding logits, or geometric resizing. Predicted score is not a guarantee of mask correctness.

## Plan and proof

Implement only the typed component above. Independent review precedes publication. Validate both worked examples, documented errors and boundaries, stable layout/order, input preservation and realistic batches. Use actual isolated Run/Submit checks; no performance leaderboard. Source is the paired paper card and primary URL. Original theory contains defined mathematics and a static trace-table visual with text equivalent. Runtime image digest is pending; actual local worker caps are declared.
