---
schema_version: 1
problem_id: detr-hungarian-assignment
content_version: 1.0.0
status: implemented
title: Match Object Queries with the Hungarian Algorithm
summary: Match Object Queries with the Hungarian Algorithm
type: function
difficulty: hard
estimated_minutes: 35
domains:
  - perception
topics:
  - detr
  - paper-component
paper_ids:
  - 2020-detr
paper_sections:
  - Mechanism and conventions defined in theory.md
track_ids: []
prerequisite_problem_ids:
  - detr-matching-cost
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
entrypoint: solution.match_queries
physical_contract:
  frames:
    - Explicit caller-observation conventions in statement
  units:
    features: dimensionless
  axes: 'cost(Q,M),1<=Q<=128,0<=M<=Q; result(M,), indexed by target.'
  timestamp_assumptions: One observation batch; no internal clock.
  batching: 'cost(Q,M),1<=Q<=128,0<=M<=Q; result(M,), indexed by target.'
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.e-9
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
  evaluator_sha256: 4dd92c075b65e46e2efb1c0d4885c146e370fd1d34b10ea63a7c15fab6962ef5
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original bounded teaching task. No copied source code or figure.
  primary_urls:
    - 'https://arxiv.org/abs/2005.12872'
  implementation_urls: []
  paper_card: research/papers/vision-vlm-3d/2020-detr.md
  manifest: research/manifests/vision-vlm-3d.md
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Match Object Queries with the Hungarian Algorithm

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/detr-hungarian-assignment. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Treat targets as rows and queries as columns. Maintain target/query potentials, per-column slack and predecessor columns; each new target augments the current matching through an alternating path. Potential updates expose a free query without freezing earlier assignments. Return the matched query for each target, preserving target order. The rectangular algorithm takes O(M²Q) time and O(M+Q) auxiliary storage beyond the cost array. Any tied optimum is acceptable; greedy assignment is not.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox detr-hungarian-assignment. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
