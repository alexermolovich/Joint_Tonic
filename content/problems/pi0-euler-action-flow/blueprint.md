---
schema_version: 1
problem_id: pi0-euler-action-flow
content_version: 1.0.0
status: implemented
title: Integrate an Action Flow with Euler Steps
summary: Integrate an Action Flow with Euler Steps
type: component
difficulty: medium
estimated_minutes: 35
domains:
  - VLA and embodied robot learning
topics:
  - 2024-pi0
  - policy-interface
paper_ids:
  - 2024-pi0
paper_sections:
  - 'SectionIV and AppendixA-D: forward Euler inference'
track_ids: []
prerequisite_problem_ids:
  - pi0-flow-action-interpolants
runtime:
  language: python
  python: 3.12.3
  image_digest: pending-local-worker-build
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  publication_note: >-
    Local CPU bubblewrap runtime. OCI image digest is not available;
    Python/dependencies and evaluator source hash are pinned. Shared enforced
    caps are listed below.
entrypoint: solution.euler_action_flow
physical_contract:
  frames:
    - Caller-declared normalized action interface; no frame conversion
  units:
    tokens: dimensionless integer IDs
    actions: normalized Euclidean channels
    flow_time: 'dimensionless, separate from controller timestamps'
  axes: Shapes and ordering defined explicitly in statement.md
  timestamp_assumptions: >-
    One aligned control observation per batch item; fixed horizon interval
    provided upstream
  batching: Batch-first; empty batch supported only for token grammar tasks
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - two-worked-examples
  hidden_case_families:
    - dtype-shape-range-validation
    - ordering
    - noncontiguous-and-storage
    - empty-where-supported
    - independent-oracle
    - realistic-scale
fixtures:
  source: Original deterministic synthetic examples and evaluator cases
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original bounded component contract inspired by the cited mechanism; no full
    trained policy or physical evaluation is reproduced.
  primary_urls:
    - 'https://arxiv.org/pdf/2410.24164v4'
  implementation_urls: []
owners:
  - vla_implementation
reviewers:
  - code_issue_scout
evaluator_sha256: e54f73b6681b9b972fc0ef6a98cdfec6ae210dddd5bf42c0ec8a841141aa650e
---

# Integrate an Action Flow with Euler Steps

## Learning objective

Integrate an Action Flow with Euler Steps

## Paper connection and scope

Original bounded component contract inspired by the cited mechanism; no full trained policy or physical evaluation is reproduced.

Source sections: SectionIV and AppendixA-D: forward Euler inference.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Copy the supplied initial chunk, call the field once at each interval's current state and left-endpoint time, validate the returned velocity, and construct the next state without modifying callback-owned arrays. Save each state in a separate trace and copy the final state before returning it. Time excluding the callback is O(KBHD), output storage O((K+1)BHD), and there are exactly K callback evaluations.

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
