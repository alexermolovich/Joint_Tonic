---
schema_version: 1
problem_id: bev-ego-motion-warp
content_version: 1.0.0
status: implemented
title: Warp a Previous BEV with Ego Motion
summary: Warp a Previous BEV with Ego Motion
type: function
difficulty: hard
estimated_minutes: 40
domains:
  - perception
topics:
  - bevformer
  - paper-component
paper_ids:
  - 2022-bevformer
paper_sections:
  - Mechanism and explicit teaching conventions in theory.md
track_ids: []
prerequisite_problem_ids:
  - se3-transform-points
runtime:
  language: python
  python: 3.12.3
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
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
entrypoint: solution.warp_previous_bev
physical_contract:
  frames:
    - Explicit caller grid/view frames in statement
  units:
    features: dimensionless; BEV geometry in metres where stated
  axes: 'previous(H,W,C), previous_from_current(3,3), origin(2,); output(H,W,C).'
  timestamp_assumptions: One explicitly paired batch; no internal clock.
  batching: 'previous(H,W,C), previous_from_current(3,3), origin(2,); output(H,W,C).'
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - worked-examples
    - minimal-shape
  hidden_case_families:
    - validation
    - edge-policy
    - layout
    - preservation
    - independent-oracle
    - scale
  performance_class: cpu
  evaluator_sha256: af2500673cdfed29e98ac3c1460af262df83c6c318f8094aa2da2003e222ec13
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original bounded teaching task; variants explicitly distinguished from full
    paper systems.
  primary_urls:
    - 'https://arxiv.org/abs/2203.17270'
  implementation_urls: []
  paper_card: research/papers/vision-vlm-3d/2022-bevformer.md
  manifest: research/manifests/vision-vlm-3d.md
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Warp a Previous BEV with Ego Motion

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/bev-ego-motion-warp. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Use inverse lookup from current cell centers into the previous grid. Algebraically compute fractional index coordinates as R@[c+.5,r+.5]+((R-I)@origin+t)/resolution-.5; this avoids subtracting two large metric origins for identity motion. For each of four integer neighbors, add its bilinear contribution only where that neighbor is inside the grid. Do not clamp, wrap or renormalize. Output storage is independent, and complexity is O(HWC).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox bev-ego-motion-warp. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
