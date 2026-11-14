---
schema_version: 1
problem_id: normalize-multiply-quaternions
content_version: 1.0.0
status: implemented
title: Normalize and Multiply Quaternions
summary: Normalize and Multiply Quaternions
type: function
difficulty: medium
estimated_minutes: 25
domains:
  - robotics-foundations
topics:
  - frames
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
entrypoint: solution.compose_quaternions
physical_contract:
  frames:
    - one-fixed-right-handed-Cartesian-basis
  units:
    quaternions: dimensionless
  axes: 'Hamilton scalar-first (w,x,y,z), active right-handed rotations.'
  timestamp_assumptions: One synchronized measurement clock; no offset correction.
  batching: 'Two real(4,) inputs; one float64(4,) output, no batching.'
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
  evaluator_sha256: d8f91f1fc394a7a49cc9f4c66b26ddc5b646681ca42eb100d4b7fcb73e06701f
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original robotics-foundation exercise; no paper headline result or external
    dataset.
  primary_urls:
    - >-
      https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.__mul__.html
  implementation_urls: []
owners:
  - main-agent
reviewers:
  - perception_implementation
---

# Normalize and Multiply Quaternions

## Contract

Implement **compose_quaternions(q_after, q_before)** for active right-handed rotations in one fixed Cartesian basis. Each input is a finite real integer/floating array-like of shape (4,), in scalar-first Hamilton order [w,x,y,z]. Component magnitudes must be <=1e6 and at least one component must be nonzero. Reject bool, complex, string and object dtypes.

Normalize both inputs using a scale-safe norm (divide by max(abs(q)) before taking the norm). Return a new float64 unit quaternion representing q_before followed by q_after, using the Hamilton product. Normalize the product once more. Preserve its computed sign: do not force w>=0 or flip either input. Thus negating exactly one input negates the output while leaving the represented rotation unchanged.

No batching, translation, timestamp estimation or frame conversion. The rotations describe the same static coordinate basis. Every documented violation raises ValueError; preserve inputs and independent output storage. Tiny nonzero float64 quaternions such as [1e-300,0,0,0] are valid.

## Implementation and grading plan

Reference and tests follow independent contract review. Verify worked examples, documented boundaries/errors, dtype/shape, input preservation and synthetic batches. Run public and hidden tests in the existing isolated CPU worker. Limits above are actual shared worker limits; the local image digest remains pending.

## Theory and visualization

See theory.md for intuition, defined equations, numerical trace tables and robot failure analysis. Static tables need no reduced-motion variant.

## Provenance and operations

Fixtures are original synthetic CC0-1.0 data. Record content/runtime versions and sensor/calibration versions where relevant. No simulator, GPU, hosted service or external dataset is needed.
