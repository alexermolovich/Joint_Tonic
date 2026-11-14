---
schema_version: 1
problem_id: class-aware-nms
content_version: 1.0.0
status: implemented
title: Run Class-Aware Non-Maximum Suppression
summary: Remove redundant detections while retaining distinct classes and deterministic ties.
type: component
difficulty: medium
estimated_minutes: 35
domains: [perception]
topics: [nms, iou, detection-postprocessing]
paper_ids: [2016-yolo-v1]
paper_sections: ['Section 2 and detection postprocessing context']
track_ids: [geometry-detection-foundations]
prerequisite_problem_ids: [box-iou-broadcast]
runtime:
  language: python
  python: '3.12'
  image_digest: pending-local-worker-build
  dependencies: {numpy: '2.2.4'}
  limits: {wall_seconds: 2, cpu_seconds: 2, memory_mb: 256, output_kb: 64}
entrypoint: solution.class_aware_nms
physical_contract:
  frames: [shared-image-plane]
  units: {boxes: pixels, scores: dimensionless, threshold: dimensionless}
  axes: continuous xyxy; x-right y-down
  timestamp_assumptions: one image at one time
  batching: boxes (N,4), scores (N,), class_ids (N,)
grading:
  mode: exact
  seed: 20261113
  rtol: 1.0e-7
  atol: 1.0e-9
  public_case_families: [same-class, different-class, empty]
  hidden_case_families: [ties, threshold-equality, degenerate, greedy-chain, many-classes, scale, invalid-shapes-ranges, immutability]
  performance_class: cpu-vectorized-per-candidate
fixtures: {source: synthetic, license: CC0-1.0, version_or_hash: synthetic-v1-seed-20261113}
provenance:
  authoring_notes: Original class-aware greedy NMS task; NMS is a shared pipeline technique, not YOLO's novel contribution.
  primary_urls: [https://arxiv.org/abs/1506.02640]
  implementation_urls: []
owners: [joint-tonic-content]
reviewers: []
---

# Run Class-Aware Non-Maximum Suppression

## Learning objective

Implement deterministic greedy postprocessing and distinguish same-class redundancy from cross-class overlap.

## Paper connection and scope

Companion to the YOLO decoder and the original YOLO detection pipeline. This is a general postprocessing operation, not a reproduction of the network or a claim that NMS originated with YOLO.

## Contract

`class_aware_nms(boxes,scores,class_ids,iou_threshold=0.5)` accepts finite real `(N,4)` xyxy boxes (magnitudes <=1e6, non-reversed), finite scores `(N,)` in `[0,1]`, and nonnegative integer class IDs `(N,)`. Numerically integral float IDs are accepted; booleans are rejected. Threshold is finite `[0,1]`. Zero-area boxes are allowed and have IoU zero. Choose highest score, break ties by lower original index, and suppress only remaining same-class candidates whose IoU is strictly greater than threshold. Return kept Python integer original indices in greedy order. Empty arrays are supported. Invalid input raises ValueError; preserve inputs.

## Learner prompt draft

Use each kept detection to remove redundant same-class candidates, never letting an already-suppressed candidate suppress another box.

## Worked examples

Two identical class-0 boxes with scores .9 and .8 retain `[0]` at threshold .5. If the second box is class 1, retain `[0,1]`. At threshold 1.0 even identical boxes are retained because equality is not suppression.

## Starter-code plan

Expose `class_aware_nms(...)`; TODO validation, stable ordering, vectorized overlap, and iterative filtering.

## Reference-solution plan

Stable descending sort, repeatedly retain the first candidate, compute its IoU with remaining boxes, and remove only high-overlap matching classes. Worst-case O(N^2) time with O(N) additional state.

## Evaluator plan

| Case family | Public/hidden | Invariant | Tolerance | Why |
|---|---|---|---|---|
| Same/different class and empty | Public | Index sequence | Exact | Basic behavior |
| Equal scores/IoU equality | Hidden | Tie and cutoff policies | Exact | Reproducible serving |
| Greedy chain/degenerate/multi-class | Hidden | Correct suppression graph | Exact | Avoid over-suppression |
| Invalid/immutable/scale | Hidden | Contract | Exact | Robust integration |

No external fixtures or stochastic timing assertions. Resolve worker image digest before publication.

## Visualization plan

`nms` steps through chosen/suppressed candidates and an IoU row; also provide a kept/suppressed index table and manual step controls for reduced motion.

## Theory and hints

Teach greedy selection with class-conditioned edges. Hint 1: sort once with stable ties. Hint 2: remove suppressed candidates before selecting again. Common failure: comparing all pairs at once and removing boxes based on an already-discarded neighbor.

## MLOps/reproducibility extension

Version threshold, class mapping, tie policy, and coordinate convention to compare edge and training-framework outputs reliably.

## Editorial checklist

- [x] Complete original prompt/theory, metadata, solution, and public/hidden tests present.
- [ ] Pin evaluator image and independent correctness/accessibility review before publication.
