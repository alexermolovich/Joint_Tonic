---
schema_version: 1
problem_id: planar-two-link-ik
content_version: 1.0.0
status: implemented
title: Solve Closed-Form IK for a Planar Two-Link Arm
summary: Solve Closed-Form IK for a Planar Two-Link Arm
type: function
difficulty: medium
estimated_minutes: 25
domains:
  - robotics-foundations
topics:
  - kinematics
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
entrypoint: solution.planar_ik
physical_contract:
  frames:
    - base
    - link1
    - link2
    - tool
  units:
    lengths: meters
    target: meters
    angles: radians
  axes: 'Base x right, y up; positive joint rotations about +z, counterclockwise.'
  timestamp_assumptions: One synchronized measurement clock; no offset correction.
  batching: 'Two scalar lengths and one target(2,); one result dict.'
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.e-7
  atol: 1.e-7
  public_case_families:
    - worked-examples
  hidden_case_families:
    - boundary
    - validation
    - empty-where-supported
    - immutability
    - scale
  performance_class: cpu
  evaluator_sha256: 948435040538c4ea772707c1248f9d488ffa61843ec1228da4dfdd196be28649
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original robotics-foundation exercise; no paper headline result or external
    dataset.
  primary_urls:
    - 'https://hades.mech.northwestern.edu/images/7/7e/MR-2up-v2.pdf'
  implementation_urls: []
owners:
  - main-agent
reviewers:
  - perception_implementation
---

# Solve Closed-Form IK for a Planar Two-Link Arm

## Contract

Implement **planar_ik(L1, L2, target)**. L1 and L2 are real Python/NumPy scalars, excluding bool, in [1e-3,1e3] meters, with max(L1,L2)/min(L1,L2)<=1000. target is a finite real integer/floating array-like (2,) with per-coordinate magnitude <=1e6 meters; reject bool, complex, string and object dtypes.

Return a dict with exactly reachable (Python bool), angles (None or a new float64 (2,) array), and singular (Python bool). The shoulder angle q1 is normalized into [-pi,pi); relative elbow angle q2 is in [0,pi]. Positive angles rotate counterclockwise about base +z.

Let r=hypot(x,y). Targets below abs(L1-L2)-1e-9 or above L1+L2+1e-9 are unreachable: return False,None,False. For the tolerance band, clamp the law-of-cosines result to [-1,1] after this reachability test. For reachable targets q2=acos((r*r-L1*L1-L2*L2)/(2*L1*L2)); q1=atan2(y,x)-atan2(L2*sin(q2),L1+L2*cos(q2)). Mark singular when abs(sin(q2))<=1e-9. For exactly equal lengths and exact target [0,0], choose q1=0,q2=pi.

Raise ValueError for every documented invalid input; preserve inputs. This is one static geometric branch, without joint limits, obstacles, tool orientation or continuity across calls. Numerical results use atol=1e-7 radians and rtol=1e-7, away from tolerance-boundary classification. No simulator is required; the planned MuJoCo sidecar is separate.

## Implementation and grading plan

Reference and tests follow independent contract review. Verify worked examples, documented boundaries/errors, dtype/shape, input preservation and synthetic batches. Run public and hidden tests in the existing isolated CPU worker. Limits above are actual shared worker limits; the local image digest remains pending.

## Theory and visualization

See theory.md for intuition, defined equations, numerical trace tables and robot failure analysis. Static tables need no reduced-motion variant.

## Provenance and operations

Fixtures are original synthetic CC0-1.0 data. Record content/runtime versions and sensor/calibration versions where relevant. No simulator, GPU, hosted service or external dataset is needed.
