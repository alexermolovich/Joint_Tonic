---
schema_version: 1
problem_id: sam-stability-overlap-filter
content_version: 1.0.0
status: implemented
title: Filter Automatic Masks by Stability and Overlap
summary: Filter Automatic Masks by Stability and Overlap
type: function
difficulty: hard
estimated_minutes: 40
domains:
  - perception
topics:
  - segment-anything
  - paper-component
paper_ids:
  - 2023-segment-anything
paper_sections:
  - Mechanism and explicit teaching conventions in theory.md
track_ids: []
prerequisite_problem_ids:
  - sam-mask-ranking
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
entrypoint: solution.filter_stable_masks
physical_contract:
  frames:
    - Explicit caller grid/view frames in statement
  units:
    features: dimensionless; BEV geometry in metres where stated
  axes: 'logits(N,H,W), quality(N); output original candidate indices(K).'
  timestamp_assumptions: One explicitly paired batch; no internal clock.
  batching: 'logits(N,H,W), quality(N); output original candidate indices(K).'
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
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
  evaluator_sha256: e733a62892bf43be62ab295c5c1bac872e8b3ef285da5baf02645a80ae771175
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original bounded teaching task; variants explicitly distinguished from full
    paper systems.
  primary_urls:
    - 'https://arxiv.org/abs/2304.02643'
  implementation_urls: []
  paper_card: research/papers/vision-vlm-3d/2023-segment-anything.md
  manifest: research/manifests/vision-vlm-3d.md
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Filter Automatic Masks by Stability and Overlap

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/sam-stability-overlap-filter. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Threshold each logit mask at the base and perturbed levels. Compute high/low count ratios with the declared empty policy and discard empty or unstable base masks before ranking. Sort eligible indices by descending quality and original index, then greedily compare each candidate only with kept binary masks. Suppress strictly above the mask-IoU threshold. This is the specified mask-overlap variant, not SAM box NMS. Worst-case work is O(N²HW), with O(NHW) mask storage.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox sam-stability-overlap-filter. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
