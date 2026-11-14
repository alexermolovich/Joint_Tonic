---
schema_version: 1
problem_id: unproject-depth-map
content_version: 1.0.0
status: implemented
title: Unproject a Depth Map into a Point Cloud
summary: Unproject a Depth Map into a Point Cloud
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - robotics-foundations
topics:
  - sensing
paper_ids: []
paper_sections: []
track_ids: []
prerequisite_problem_ids:
  - project-camera-points
runtime:
  language: python
  python: 3.12.3
  image_digest: pending-local-worker-build
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
entrypoint: solution.unproject_depth
physical_contract:
  frames:
    - camera-optical
  units:
    depth: meters along camera z
    K: pixels
    points: meters
  axes: 'Camera x right, y down, z forward; u column, v row.'
  timestamp_assumptions: One synchronized measurement clock; no offset correction.
  batching: 'depth(H,W), K(3,3), points(H*W,3), valid(H*W); H,W may be zero.'
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.e-7
  atol: 1.e-9
  public_case_families:
    - worked-examples
  hidden_case_families:
    - boundary
    - validation
    - empty-where-supported
    - immutability
    - scale
  performance_class: cpu
  evaluator_sha256: 7d569a4e45496ba66370bef94235c283c1c272719c260e6e0868449fddfa7d06
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original robotics-foundation exercise; no paper headline result or external
    dataset.
  primary_urls:
    - 'https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html'
  implementation_urls: []
owners:
  - main-agent
reviewers:
  - code_issue_scout
---

# Unproject a Depth Map into a Point Cloud

## Contract

Implement **unproject_depth(depth, K)**.

Accept real integer/floating array-like depth (H,W); either dimension may be zero. Depth is optical-axis z in meters, not Euclidean distance along a viewing ray. Values <=0, NaN, or either infinity indicate missing depth rather than an input error. Finite depth magnitudes must be <=1e6.

K is finite real (3,3), equal within atol=1e-9 and rtol=0 to [[fx,0,cx],[0,fy,cy],[0,0,1]], with 1e-6<=fx,fy<=1e6 and abs(cx),abs(cy)<=1e6. Reject bool, string, object, and complex arrays. All malformed inputs raise ValueError.

Return new float64 points (H*W,3) and bool valid (H*W,) in C row-major order. Pixel centers use integer (u=column,v=row), with no half-pixel offset. Positive finite depths produce [(u-cx)*z/fx,(v-cy)*z/fy,z] in the camera optical frame. Missing depths produce three NaNs and false. Preserve inputs and independent output storage.

All pixels are one static exposure. No distortion, world transform, depth-hole filling or occlusion reasoning.

## Implementation and grading plan

Reference and tests follow independent contract review. Verify worked examples, documented boundaries/errors, dtype/shape, input preservation and synthetic batches. Run public and hidden tests in the existing isolated CPU worker. Limits above are actual shared worker limits; the local image digest remains pending.

## Theory and visualization

See theory.md for intuition, defined equations, numerical trace tables and robot failure analysis. Static tables need no reduced-motion variant.

## Provenance and operations

Fixtures are original synthetic CC0-1.0 data. Record content/runtime versions and sensor/calibration versions where relevant. No simulator, GPU, hosted service or external dataset is needed.
