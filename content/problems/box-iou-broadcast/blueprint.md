---
schema_version: 1
problem_id: box-iou-broadcast
content_version: 1.0.0
status: implemented
title: Compute Pairwise Bounding-Box IoU
summary: Compare every box in two sets using vectorized intersection over union.
type: function
difficulty: easy
estimated_minutes: 20
domains: [perception]
topics: [bounding-boxes, iou, broadcasting]
paper_ids: [2016-yolo-v1]
paper_sections: ['Section 2: confidence and overlap interpretation']
track_ids: [geometry-detection-foundations]
prerequisite_problem_ids: []
runtime:
  language: python
  python: '3.12'
  image_digest: pending-local-worker-build
  dependencies: {numpy: '2.2.4'}
  limits: {wall_seconds: 2, cpu_seconds: 2, memory_mb: 256, output_kb: 64}
entrypoint: solution.pairwise_iou
physical_contract:
  frames: [shared-image-plane]
  units: {coordinates: pixels, overlap: dimensionless}
  axes: x-right y-down; continuous xyxy boxes
  timestamp_assumptions: both sets describe one image
  batching: boxes_a (N,4), boxes_b (M,4), output (N,M)
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.0e-7
  atol: 1.0e-9
  public_case_families: [identity, disjoint, partial-overlap]
  hidden_case_families: [empty, zero-area, touching, containment, symmetry, translation, reversed, nonfinite, immutability]
  performance_class: cpu-vectorized-pairs
fixtures: {source: synthetic, license: CC0-1.0, version_or_hash: synthetic-v1-seed-20261113}
provenance:
  authoring_notes: Original geometric exercise, a prerequisite used in detection pipelines.
  primary_urls: [https://arxiv.org/abs/1506.02640]
  implementation_urls: []
owners: [joint-tonic-content]
reviewers: []
---

# Compute Pairwise Bounding-Box IoU

## Learning objective

Use broadcasting to compare two independently sized sets without loops over pairs.

## Paper connection and scope

YOLO v1 Section 2 uses IoU to express confidence and overlap. This task teaches the shared geometry, without implementing the detector or reproducing its experiments.

## Contract

`pairwise_iou(boxes_a,boxes_b)` accepts finite real arrays `(N,4)` and `(M,4)` in continuous `[x1,y1,x2,y2]` coordinates, with each coordinate magnitude at most `1e6`. Require `x2>=x1,y2>=y1`; raise `ValueError` otherwise, or on bad shape/nonfinite data. Zero-area boxes are valid and have IoU zero, including with themselves. Empty `(0,4)` sets are supported. Return a float64 `(N,M)` matrix in `[0,1]`; preserve input storage. No inclusive-pixel +1 is used.

## Learner prompt draft

Compute each intersection area, each union area, and divide safely while preserving the two box-set axes.

## Worked examples

`[0,0,2,2]` compared with itself gives 1. Compared with `[1,1,3,3]`, intersection is 1 and union 7, yielding `1/7`. Boxes meeting at one edge have zero overlap.

## Starter-code plan

Expose `pairwise_iou(boxes_a,boxes_b)` with TODOs for validation, broadcasting, and safe division.

## Reference-solution plan

Expand set axes to `(N,1,2)` and `(1,M,2)`. Clamp intersection extents at zero, broadcast areas, and use masked division for zero unions. O(NM) time and memory.

## Evaluator plan

| Case family | Public/hidden | Invariant | Tolerance | Why |
|---|---|---|---|---|
| Identity/disjoint/overlap | Public | Analytic fraction | Declared above | Core formula |
| Degenerate/empty/touching | Hidden | Zero behavior and shapes | Exact | Safe postprocessing |
| Symmetry/translation/scale | Hidden | Geometry invariance | Declared above | Catch accidental axis coupling |
| Invalid/immutable | Hidden | Contract | Exact | Stable downstream behavior |

Seeded fixtures never use external images. Performance is represented by a moderate matrix-shape case, not noisy stopwatch grading. Worker image is pending build.

## Visualization plan

`iou` displays two boxes with intersection/union shading and a live score matrix. A numeric area table provides an accessible alternative.

## Theory and hints

Derive intersection bounds before union. Hint: `a[:,None,:]` and `b[None,:,:]` expose independent box axes. Common failure: adding one to continuous widths.

## MLOps/reproducibility extension

Declare box conventions in exported model metadata; a coordinate-convention change can alter both evaluation and suppression.

## Editorial checklist

- [x] Paper link, original content, fixture license, solution, and tests present.
- [ ] Resolve container digest and independent review before publication.
