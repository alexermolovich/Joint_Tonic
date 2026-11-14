---
schema_version: 1
problem_id: detr-matching-cost
content_version: 1.0.0
status: implemented
title: Build a Detection Bipartite-Matching Cost Matrix
summary: >-
  Build pairwise query-to-target costs from class probabilities, normalized box
  distances, and generalized IoU.
type: function
difficulty: medium
estimated_minutes: 50
domains:
  - perception
topics:
  - object-detection
  - set-prediction
  - generalized-iou
paper_ids:
  - 2020-detr
paper_sections:
  - 'Section 3.1: object detection set prediction loss; Appendix A.2: box loss'
track_ids: []
prerequisite_problem_ids:
  - box-iou-broadcast
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  platform: linux-x86_64-cpu
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.detr_matching_cost
physical_contract:
  frames:
    - normalized image plane
  units:
    boxes: dimensionless image fractions
    probabilities: dimensionless
    cost: dimensionless
  axes: 'x increases right; y increases down; boxes are (cx,cy,width,height).'
  timestamp_assumptions: >-
    No timestamp input; any temporal or scene alignment is an upstream caller
    responsibility.
  batching: 'One image per call. Q queries, M real targets; no padding or batch axis.'
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - identical and touching boxes
    - disjoint boxes with negative GIoU
    - empty target set
  hidden_case_families:
    - background label rejected
    - repeated classes and unequal Q/M
    - individual cost weights disabled
    - noncontiguous inputs and invalid dtype/range
    - corner extension without clipping
  performance_class: none
  evaluator_sha256: 862b80338d7f4befc8140e63c5535fe1d03f8ee37f538ba9bb6bf1da1fedccfb
fixtures:
  source: >-
    original synthetic examples in examples.md; future generated fixtures use
    declared seed
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original bounded teaching contract and explanations; source mechanisms
    checked against the paired paper card and primary sources; no paper figures
    or implementation code copied.
  primary_urls:
    - 'https://arxiv.org/abs/2005.12872'
  implementation_urls:
    - 'https://github.com/facebookresearch/detr/blob/main/models/matcher.py'
owners:
  - ui_issue_scout
reviewers:
  - paper_explanations
---
# Build a Detection Bipartite-Matching Cost Matrix

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/detr-matching-cost. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate all inputs, including an empty target set. Convert center-size boxes to corners only for geometry. Broadcast query and target corners to compute intersection, union, and enclosing areas; GIoU is IoU minus uncovered enclosure fraction. Compute L1 in the original center-size space and index target class probabilities. Combine negative probability, L1, and negative GIoU with the supplied weights. The result is Q×M; the assignment itself is a separate problem. Time and auxiliary memory are O(QM), after validating probabilities.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox detr-matching-cost. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
