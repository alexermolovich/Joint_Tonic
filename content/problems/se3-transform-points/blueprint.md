---
schema_version: 1
problem_id: se3-transform-points
content_version: 1.0.0
status: implemented
title: Apply an SE(3) Transform to Batched Points
summary: Move camera-frame points into the world frame with one rigid transform.
type: function
difficulty: easy
estimated_minutes: 20
domains: [geometry]
topics: [se3, coordinate-frames, vectorization]
paper_ids: []
paper_sections: []
track_ids: [geometry-detection-foundations]
prerequisite_problem_ids: []
runtime:
  language: python
  python: '3.12'
  image_digest: pending-local-worker-build
  dependencies: {numpy: '2.2.4'}
  limits: {wall_seconds: 2, cpu_seconds: 2, memory_mb: 256, output_kb: 64}
entrypoint: solution.transform_points
physical_contract:
  frames: [camera, world]
  units: {translation: meters, points: meters, rotation: dimensionless}
  axes: right-handed; camera input and world output use their declared local axes
  timestamp_assumptions: static transform and synchronized points
  batching: one point (3,) or row-major batch (N,3), including N=0
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.0e-7
  atol: 1.0e-9
  public_case_families: [identity, translation, rotation]
  hidden_case_families: [composition, inverse, empty, dtype, input-mutation, invalid-shapes, invalid-rigid-transform, nonfinite]
  performance_class: cpu-vectorized
fixtures: {source: synthetic, license: CC0-1.0, version_or_hash: 'synthetic-v1-seed-20261113'}
provenance:
  authoring_notes: Original numerical exercise based on standard rigid-body geometry.
  primary_urls: [https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/]
  implementation_urls: []
owners: [joint-tonic-content]
reviewers: []
---

# Apply an SE(3) Transform to Batched Points

## Learning objective

Translate a physical frame convention into a vectorized array operation without transposing the transform direction.

## Paper connection and scope

This is a shared geometry prerequisite, rather than a paper reproduction. The linked Modern Robotics author resource establishes the homogeneous-transform convention. It supports later camera, policy, and simulator tasks.

## Contract

`transform_points(T, points)` accepts finite real numeric arrays: a proper rigid transform `(4,4)` from camera to world and points `(3,)` or `(N,3)` in meters. Return independent float64 storage of the same point shape. Require bottom row `[0,0,0,1]`, orthonormal rotation, and determinant +1, using absolute tolerance `1e-7` and zero relative tolerance. Raise `ValueError` for malformed/nonfinite inputs. Preserve input arrays.

## Learner prompt draft

Apply rotation and then translation to each point. Preserve whether the caller supplied one point or a batch. Use array operations for the batch.

## Worked examples

Identity sends `[1,2,3]` to `[1,2,3]`. A transform with identity rotation and translation `[1,-2,3]` sends `[[0,0,0],[2,1,-1]]` to `[[1,-2,3],[3,-1,2]]`.

## Starter-code plan

`starter.py` exposes `transform_points(T, points)` with a focused TODO for validation and the batched operation.

## Reference-solution plan

Convert to float64, validate, and use `points @ R.T + t`. Time and output memory are O(N).

## Evaluator plan

| Case family | Public/hidden | Invariant | Tolerance | Why |
|---|---|---|---|---|
| Identity/translation/rotation | Public | Known coordinates | Declared above | Establish direction |
| Composition/inverse/large batch | Hidden | Rigid-map consistency | Declared above | Catch transpose and batching errors |
| Invalid/empty/immutable inputs | Hidden | Contract | Exact | Stable integration |

Seeded fixtures make every result reproducible. The evaluator reports import/runtime failures separately from assertions. Container digest is intentionally pending the worker image build; this is not published content yet.

## Visualization plan

The `transform` adapter draws camera/world axes, original and transformed points, and a translation arrow. A coordinate table is the text alternative.

## Theory and hints

Explain frames before matrix multiplication. Hint 1: extract the upper-left rotation and last-column translation. Hint 2: row-batched points multiply the transpose. Main failure: confusing camera-to-world with world-to-camera.

## MLOps/reproducibility extension

Version frame names and calibration alongside model checkpoints so changing extrinsics cannot silently move a grasp target.

## Editorial checklist

- [x] Contract, examples, original explanation, synthetic fixtures, and evaluator implemented.
- [ ] Worker container digest pinned after build.
- [ ] Independent subject and accessibility review before publication.
