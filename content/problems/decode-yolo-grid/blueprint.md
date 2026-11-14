---
schema_version: 1
problem_id: decode-yolo-grid
content_version: 1.0.0
status: implemented
title: Decode YOLO Grid Predictions
summary: Turn grid-relative detections into deterministic image-space boxes and class scores.
type: component
difficulty: medium
estimated_minutes: 40
domains: [perception]
topics: [yolo, detection-codecs, grid-decoding]
paper_ids: [2016-yolo-v1]
paper_sections: ['Section 2: unified detection and grid-relative representation']
track_ids: [geometry-detection-foundations]
prerequisite_problem_ids: [project-camera-points, box-iou-broadcast]
runtime:
  language: python
  python: '3.12'
  image_digest: pending-local-worker-build
  dependencies: {numpy: '2.2.4'}
  limits: {wall_seconds: 2, cpu_seconds: 2, memory_mb: 256, output_kb: 64}
entrypoint: solution.decode_yolo
physical_contract:
  frames: [image-grid, image-pixels]
  units: {offsets: cell-fractions, size: image-fractions, box: pixels, score: dimensionless}
  axes: columns x-right and rows y-down
  timestamp_assumptions: predictions belong to one image
  batching: predictions (Sy,Sx,B,5+C); one image; C>=1
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.0e-7
  atol: 1.0e-9
  public_case_families: [single-cell, multi-class, filtered-empty]
  hidden_case_families: [rectangular-grid-image, multi-box, ties, clipping, zero-area, threshold-equality, invalid-range, malformed, immutability]
  performance_class: cpu-bounded-grid
fixtures: {source: synthetic, license: CC0-1.0, version_or_hash: synthetic-v1-seed-20261113}
provenance:
  authoring_notes: Original teaching codec inspired by YOLO v1; direct normalized sizes and per-box class channels are explicitly chosen for this exercise.
  primary_urls: [https://arxiv.org/abs/1506.02640]
  implementation_urls: []
owners: [joint-tonic-content]
reviewers: []
---

# Decode YOLO Grid Predictions

## Learning objective

Convert coordinate conventions and calibrated class confidence into a stable detector output interface.

## Paper connection and scope

Inspired by YOLO v1 Section 2 grid-relative predictions. The exercise deliberately uses direct image-normalized width/height and per-box class channels, rather than copying the full original output layout, training loss, or later YOLO codecs. It performs decoding only; NMS is a separate problem.

## Contract

`decode_yolo(predictions,image_size,score_threshold=0.25)` accepts finite real `(Sy,Sx,B,5+C)` values in `[0,1]`, positive Sy/Sx/B, C>=1. Channels are `tx,ty,w,h,objectness,class_0,...`; sizes are direct fractions, not log or square-root encodings. `image_size=(width,height)` uses positive integers, excluding booleans. Threshold is finite `[0,1]`. For every cell/box/class, emit score `objectness*class_probability` when `score>=threshold`, clip xyxy to image edges, and skip zero-area boxes. Output list dictionaries contain `box` as four Python floats, `class_id` as int, `score` as float. Sort descending by score; ties preserve row/column/box/class traversal order. Raise `ValueError` for invalid inputs and do not mutate them.

## Learner prompt draft

Decode a complete image's grid predictions while preserving class-specific scores and deterministic ordering.

## Worked examples

For a 100x80 image, one cell with `[.5,.5,.4,.5,.8,.75]` emits `[30,20,70,60]`, class 0, score .6. Changing objectness to .2 makes its .15 score fall below the default threshold, producing an empty list.

## Starter-code plan

Expose `decode_yolo(predictions,image_size,score_threshold=0.25)`; leave validation, coordinates, score filtering, and stable ordering as TODOs.

## Reference-solution plan

Walk bounded grid entries or vectorize them. Compute center from row/column and offsets, scale widths/heights by the image dimensions, clip, then emit valid class scores. O(Sy*Sx*B*C) generation plus O(D log D) sorting for D emitted detections.

## Evaluator plan

| Case family | Public/hidden | Invariant | Tolerance | Why |
|---|---|---|---|---|
| Single/multi-class/filter | Public | Box and scores | Declared above | Full output contract |
| Rectangular/clip/multi-box | Hidden | Independent axes and extents | Declared above | Avoid square-only shortcuts |
| Threshold/ties/zero-area | Hidden | Stable exact policy | Exact order | Reproducibility |
| Invalid inputs | Hidden | ValueError and immutability | Exact | Model-interface hygiene |

Small synthetic prediction tensors are original CC0 fixtures. Worker container digest awaits build; no noisy speed threshold is used.

## Visualization plan

`yolo` overlays the grid, selected cell, center offsets, decoded rectangle, and class-score product. A row table gives every intermediate value.

## Theory and hints

Connect the cell-local center to pixel-space center before xyxy conversion. Hint 1: x uses column/Sx and width. Hint 2: filter the product, not the class probability alone. Common failure: silently applying a different YOLO version's size codec.

## MLOps/reproducibility extension

Serialize codec version, class order, score threshold, image preprocessing, and clipping policy together with the model artifact.

## Editorial checklist

- [x] Original codec and deviations documented, examples/test fixtures implemented.
- [ ] Pin evaluator image and obtain independent correctness/accessibility review.
