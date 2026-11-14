---
schema_version: 1
problem_id: bev-weighted-camera-features
content_version: 1.0.0
status: implemented
title: Aggregate Multi-Camera Features with Attention Weights
summary: Aggregate Multi-Camera Features with Attention Weights
type: function
difficulty: easy
estimated_minutes: 30
domains:
  - perception
topics:
  - bevformer
  - paper-component
paper_ids:
  - 2022-bevformer
paper_sections:
  - Mechanism and limits stated in theory.md
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.aggregate_camera_features
physical_contract:
  frames:
    - Contract declares observation and coordinate assumptions
  units:
    features: dimensionless; ray distances in meters where applicable
  axes: >-
    features(B,Q,C,S,D),weights(B,Q,C,S),valid(B,Q,C,S);
    output(B,Q,D),observed(B,Q).
  timestamp_assumptions: One synchronized upstream observation or training snapshot.
  batching: >-
    features(B,Q,C,S,D),weights(B,Q,C,S),valid(B,Q,C,S);
    output(B,Q,D),observed(B,Q).
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.e-7
  atol: 1.e-9
  public_case_families:
    - worked-examples
    - minimal-shape
  hidden_case_families:
    - validation
    - empty-policy
    - noncontiguous
    - immutability
    - numerical-boundaries
    - independent-oracle
  performance_class: none
  evaluator_sha256: 7aa57f4c3426953f68b2c7ecb3d4276b59659f5542df334952b91127cb127af4
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original scoped exercise; no paper figure/prose/code copied.
  primary_urls:
    - 'https://arxiv.org/abs/2203.17270'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Aggregate Multi-Camera Features with Attention Weights

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/bev-weighted-camera-features. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Zero invalid weights and find the maximum remaining weight per query. Divide by that maximum before normalization: this preserves the mathematical mean while preventing very small positive weights from underflowing when multiplied by features. Normalize over camera and sample axes, then reduce weighted features over the same axes. Queries with no positive mass return zeros and false. Time and temporary storage are O(BQCSD).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox bev-weighted-camera-features. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
