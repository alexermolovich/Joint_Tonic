---
schema_version: 1
problem_id: compose-frame-transforms
content_version: 1.0.0
status: reviewed
title: Compose and Invert Coordinate Transforms
summary: Compose and Invert Coordinate Transforms
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
entrypoint: solution.compose_transforms
physical_contract:
  frames:
    - a
    - b
    - c
  units:
    translation: meters
    stamp: seconds
    rotation: dimensionless
  axes: Right-handed frames; transforms act on homogeneous column vectors.
  timestamp_assumptions: One synchronized measurement clock; no offset correction.
  batching: Two transform records; no batch dimension.
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
      https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/
  implementation_urls: []
owners:
  - main-agent
reviewers:
  - perception_implementation
---

# Compose and Invert Coordinate Transforms

## Contract

Implement **compose_transforms(first, second)**. Each input is a dict with required keys matrix, target, source, stamp and unit; ignore extra keys.

matrix is a finite real integer/floating array-like (4,4), with translation magnitude per component <=1e6. Reject bool, complex, string or object matrix dtypes. Its last row is [0,0,0,1] within atol=1e-9, rtol=0. Its rotation R satisfies R.T@R=I and det(R)=1 with the same absolute tolerance. Do not repair invalid matrices.

target and source are nonempty strings without surrounding whitespace. first.source must equal second.target. Both unit fields must equal the string "m". Each stamp is a finite real Python or NumPy scalar (not bool) in [-1e6,1e6]; stamps must be exactly equal. Validate frame/unit/time compatibility before matrix multiplication.

first means a-from-b; second means b-from-c. Return a tuple of independent float64 arrays (T_ac,T_ca), each (4,4). Compute rotation R_ac=R_ab@R_bc and translation t_ac=R_ab@t_bc+t_ab; use an exact [0,0,0,1] bottom row. Invert rigidly with rotation R_ac.T and translation -R_ac.T@t_ac. Preserve inputs and return new storage.

Every documented violation raises ValueError. Same target/source labels are permitted (including a chain that returns to its starting frame). No calibration estimation or interpolation across timestamps.

## Implementation and grading plan

Reference and tests follow independent contract review. Verify worked examples, documented boundaries/errors, dtype/shape, input preservation and synthetic batches. Run public and hidden tests in the existing isolated CPU worker. Limits above are actual shared worker limits; the local image digest remains pending.

## Theory and visualization

See theory.md for intuition, defined equations, numerical trace tables and robot failure analysis. Static tables need no reduced-motion variant.

## Provenance and operations

Fixtures are original synthetic CC0-1.0 data. Record content/runtime versions and sensor/calibration versions where relevant. No simulator, GPU, hosted service or external dataset is needed.
