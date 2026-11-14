---
schema_version: 1
problem_id: nerf-render-color-depth
content_version: 1.0.0
status: implemented
title: Render Color and Expected Depth Along a Ray
summary: Render Color and Expected Depth Along a Ray
type: function
difficulty: medium
estimated_minutes: 30
domains:
  - perception
topics:
  - nerf
  - paper-component
paper_ids:
  - 2020-nerf
paper_sections:
  - Mechanism and limits stated in theory.md
track_ids: []
prerequisite_problem_ids:
  - nerf-alpha-compositing
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
entrypoint: solution.render_rays
physical_contract:
  frames:
    - Contract declares observation and coordinate assumptions
  units:
    features: dimensionless; ray distances in meters where applicable
  axes: >-
    weights(R,S),colors(R,S,3),depths(R,S),background(R,),background_rgb(3,);
    return rgb(R,3), depth(R), valid(R).
  timestamp_assumptions: One synchronized upstream observation or training snapshot.
  batching: >-
    weights(R,S),colors(R,S,3),depths(R,S),background(R,),background_rgb(3,);
    return rgb(R,3), depth(R), valid(R).
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
  evaluator_sha256: 9d0988e3829e5f50bc17f57518dcf5d41a148d92398c54ac38d079ec20577750
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original scoped exercise; no paper figure/prose/code copied.
  primary_urls:
    - 'https://arxiv.org/abs/2003.08934'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Render Color and Expected Depth Along a Ray

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/nerf-render-color-depth. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate color ranges, sorted metric depths and the complete weight-plus-background mass. RGB is a direct weighted sum including background. Foreground depth is the sample-depth moment divided by foreground mass only where that mass exceeds the documented threshold. Fill other depths with NaN and expose validity separately. No weight renormalization is applied to color. Time and output/intermediate storage are O(RS).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox nerf-render-color-depth. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
