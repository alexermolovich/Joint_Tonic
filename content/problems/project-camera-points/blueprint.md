---
schema_version: 1
problem_id: project-camera-points
content_version: 1.0.0
status: implemented
title: Project Camera Points into Pixels
summary: Project visible camera-frame points and distinguish geometry from image validity.
type: function
difficulty: medium
estimated_minutes: 30
domains: [geometry]
topics: [camera-models, projection, masks]
paper_ids: []
paper_sections: []
track_ids: [geometry-detection-foundations]
prerequisite_problem_ids: [se3-transform-points]
runtime:
  language: python
  python: '3.12'
  image_digest: pending-local-worker-build
  dependencies: {numpy: '2.2.4'}
  limits: {wall_seconds: 2, cpu_seconds: 2, memory_mb: 256, output_kb: 64}
entrypoint: solution.project_points
physical_contract:
  frames: [camera-optical, image]
  units: {points: meters, depths: meters, pixels: pixels, intrinsics: pixels}
  axes: camera x-right y-down z-forward; pixel u-right v-down
  timestamp_assumptions: points and calibration describe one static image
  batching: points (N,3); pixels (N,2), depths (N,), valid (N,)
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.0e-7
  atol: 1.0e-9
  public_case_families: [optical-axis, off-axis, behind-camera]
  hidden_case_families: [near-zero-depth, boundary-pixels, empty, large-batch, nonfinite, invalid-intrinsics, image-size, immutability]
  performance_class: cpu-vectorized
fixtures: {source: synthetic, license: CC0-1.0, version_or_hash: synthetic-v1-seed-20261113}
provenance:
  authoring_notes: Original ideal pinhole camera exercise; distortion deliberately excluded.
  primary_urls: [https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html]
  implementation_urls: []
owners: [joint-tonic-content]
reviewers: []
---

# Project Camera Points into Pixels

## Learning objective

Keep projection, depth validity, and image bounds as separate parts of one precise contract.

## Paper connection and scope

Shared camera-model prerequisite using the pinhole convention in the official OpenCV calibration documentation. No distortion, rolling shutter, extrinsics, or occlusion test is included.

## Contract

`project_points(points, K, image_size)` accepts finite real `(N,3)` optical-frame points and a finite zero-skew pinhole intrinsic matrix `[[fx,0,cx],[0,fy,cy],[0,0,1]]` with positive focal lengths. Validate fixed entries with `atol=1e-9, rtol=0`. `image_size=(width,height)` contains positive integers, excluding booleans. Return float64 pixels/depths and bool validity. If `z<=1e-8`, both pixel coordinates are NaN and validity is false. Otherwise compute pixels even outside the image. Valid bounds are `0<=u<width` and `0<=v<height`. Preserve inputs; malformed or nonfinite input raises `ValueError`. Empty batches are supported.

## Learner prompt draft

Project points into a calibrated image and return a mask showing which projections can index that image safely.

## Worked examples

With focal lengths 100 and principal point `(50,40)`, `[0,0,2]` becomes `(50,40)`. `[1,-0.5,2]` becomes `(100,15)` and is invalid in a 100-pixel-wide image because the right bound is excluded. `[0,0,-1]` produces NaN pixels and depth -1.

## Starter-code plan

Expose `project_points(points,K,image_size)` and leave validation, masked division, and bounds as TODOs.

## Reference-solution plan

Allocate NaN output, divide only rows with sufficient depth, then combine bounds masks. O(N) time/memory. Avoid warnings caused by dividing invalid rows.

## Evaluator plan

| Case family | Public/hidden | Invariant | Tolerance | Why |
|---|---|---|---|---|
| Axis/off-axis/negative depth | Public | Known projection | Declared above | Coordinate intuition |
| Depth threshold/image edges | Hidden | Half-open and epsilon rules | Exact masks | Prevent invalid indexing |
| Empty/large/malformed | Hidden | Batch and validation | Exact shapes/errors | Integration reliability |

All fixtures are synthetic and seeded. A pending worker image digest must be resolved before publication.

## Visualization plan

`projection` links a camera-plane sketch to the image plane with a highlighted ray. A table lists 3D point, depth, pixels, and validity. Out-of-frame and behind-camera states have text labels.

## Theory and hints

Explain similar triangles, focal lengths, principal point, then depth filtering. Hint: validate z before division. Main failures: width/height reversal and allowing `u==width`.

## MLOps/reproducibility extension

Log calibration version, resolution, and invalid-depth rate so a resized image cannot silently invalidate perception geometry.

## Editorial checklist

- [x] Original content, examples, fixtures, reference, and meaningful tests implemented.
- [ ] Resolve local worker digest and perform independent publication review.
