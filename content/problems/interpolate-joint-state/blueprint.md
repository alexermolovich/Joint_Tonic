---
schema_version: 1
problem_id: interpolate-joint-state
content_version: 1.0.0
status: implemented
title: Interpolate Joint State at Camera Time
summary: Interpolate Joint State at Camera Time
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
prerequisite_problem_ids: []
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
entrypoint: solution.interpolate_joint_state
physical_contract:
  frames:
    - robot-joint-coordinates
  units:
    times: seconds on one synchronized clock
    q: 'radians, already unwrapped'
  axes: 'Each column is one joint coordinate, not a Cartesian axis.'
  timestamp_assumptions: One synchronized measurement clock; no offset correction.
  batching: 'times(T,), q(T,D), queries(M,); T>=2,D>=1,M>=0.'
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
  evaluator_sha256: 978b535d4b1aed286e076ab918c81d4097b0deef3d639608a11f00b9a54da89b
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original robotics-foundation exercise; no paper headline result or external
    dataset.
  primary_urls:
    - 'https://github.com/ros2/message_filters/blob/rolling/doc/index.rst'
  implementation_urls: []
owners:
  - main-agent
reviewers:
  - code_issue_scout
---

# Interpolate Joint State at Camera Time

## Contract

Implement **interpolate_joint_state(times, q, queries, max_gap)**.

Accept real integer/floating array-like inputs; convert computations to float64. Require finite strictly increasing times (T,), T>=2; finite joint positions q (T,D), D>=1; finite queries (M,); and a finite positive real scalar max_gap. All input magnitudes are <=1e6. Reject bool, complex, string or object arrays and booleans for max_gap with ValueError.

Times are measurement timestamps in seconds on one synchronized clock. Joint angles are radians, already unwrapped. Queries need not be sorted. Return new float64 aligned (M,D) and bool valid (M,). An exact source timestamp is valid regardless of nearby gaps. Otherwise interpolate only inside a bracket whose duration is <=max_gap. Out-of-range or excessive-gap queries get an all-NaN row and false. Empty queries return shapes (0,D) and (0,). Preserve input values and allocate independent output arrays.

No extrapolation, nearest-neighbor substitution, angle wrapping, or clock correction. Every documented contract violation raises ValueError.

## Implementation and grading plan

Reference and tests follow independent contract review. Verify worked examples, documented boundaries/errors, dtype/shape, input preservation and synthetic batches. Run public and hidden tests in the existing isolated CPU worker. Limits above are actual shared worker limits; the local image digest remains pending.

## Theory and visualization

See theory.md for intuition, defined equations, numerical trace tables and robot failure analysis. Static tables need no reduced-motion variant.

## Provenance and operations

Fixtures are original synthetic CC0-1.0 data. Record content/runtime versions and sensor/calibration versions where relevant. No simulator, GPU, hosted service or external dataset is needed.
