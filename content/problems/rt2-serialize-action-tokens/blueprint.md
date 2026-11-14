---
schema_version: 1
problem_id: rt2-serialize-action-tokens
content_version: 1.0.0
status: implemented
title: Serialize Robot Actions as Discrete Tokens
summary: Serialize Robot Actions as Discrete Tokens
type: component
difficulty: easy
estimated_minutes: 35
domains:
  - VLA and embodied robot learning
topics:
  - 2023-rt-2
  - policy-interface
paper_ids:
  - 2023-rt-2
paper_sections:
  - 'Section3.2: Robot-Action Fine-tuning'
track_ids: []
prerequisite_problem_ids:
  - rt1-action-codec
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
entrypoint: solution.serialize_action_tokens
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
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
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
    - 'https://arxiv.org/abs/2307.15818'
  implementation_urls: []
owners:
  - vla_implementation
reviewers:
  - code_issue_scout
evaluator_sha256: 5a17409800450f5720cc02c2e0151aecb72ff92c5afd9c09378d9880dd94f33a
---

# Serialize Robot Actions as Discrete Tokens

## Learning objective

Serialize Robot Actions as Discrete Tokens

## Paper connection and scope

Original bounded component contract inspired by the cited mechanism; no full trained policy or physical evaluation is reproduced.

Source sections: Section3.2: Robot-Action Fine-tuning.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Validate the bounded integer grammar and injective vocabulary, then gather one vocabulary entry per supplied action bin. Copy the termination flag into the first column without changing action channel order. Vocabulary validation is O(K log K) using uniqueness sorting, and mapping/output storage are O(BD). The mapping is supplied explicitly rather than inferred as an offset.

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
