---
schema_version: 1
problem_id: act-sliding-action-chunks
content_version: 1.0.0
status: implemented
title: Build Sliding Action Chunks with Padding Masks
summary: >-
  Extract fixed-horizon action windows from one episode while marking
  right-padding and preserving requested start order.
type: component
difficulty: medium
estimated_minutes: 35
domains:
  - VLA and embodied robot learning
topics:
  - act
  - action-chunking
  - episode-boundaries
paper_ids:
  - 2023-aloha-act
paper_sections:
  - >-
    SectionIV.A: Action Chunking and Temporal Ensemble; action-sequence
    prediction
  - 'SectionIV.B: demonstration chunks used by the conditional VAE'
track_ids: []
prerequisite_problem_ids:
  - validate-robot-episodes
runtime:
  language: python
  python: 3.12.3
  image_digest: pending-local-worker-build
  publication_note: >-
    Local CPU bubblewrap runtime. OCI image digest is not available;
    Python/dependencies and evaluator source hash are pinned. Shared enforced
    caps are listed below.
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
entrypoint: solution.sliding_action_chunks
physical_contract:
  frames:
    - Per-channel caller-declared controller frame; no coordinate transform
  units:
    actions: per-channel caller units or declared normalized coordinates
    start_indices: integer control ticks
    horizon: number of control ticks
  axes: 'actions(T,D); start_indices(S); chunks(S,H,D); valid(S,H)'
  timestamp_assumptions: >-
    Exactly one episode sampled at a fixed control period; index0 is its first
    action. No window crosses into another episode.
  batching: >-
    S is the requested-window axis, not separate episodes. Start order and
    duplicates are preserved; empty S is allowed.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - ordinary and end-of-episode windows
    - reordered duplicate starts with horizon beyond episode
  hidden_case_families:
    - empty start list
    - long horizon
    - noncontiguous arrays
    - duplicate order
    - dtype/shape/range validation
    - no aliasing
  performance_class: 'none; resource budget only, no latency ranking'
fixtures:
  source: Original deterministic synthetic examples and evaluator cases
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    ACT motivates predicting future action chunks. This exercise only builds
    supervised target windows from one recorded episode. Zero right-padding and
    True=valid masks are explicit educational conventions; no CVAE, policy
    inference, or cross-episode concatenation is implemented.
  primary_urls:
    - 'https://arxiv.org/abs/2304.13705'
  implementation_urls: []
owners:
  - Joint Tonic content
reviewers:
  - code_issue_scout
review_status:
  author: draft authored; verification recorded in review.md
  independent_subject_matter: approved by code_issue_scout
  independent_evaluator: contract approved by code_issue_scout; implementation pending
evaluator_sha256: ccb4d397668789d20f9442a9d5b5eae13fa9aecf17503018049716bceaf129bb
---

# Build Sliding Action Chunks with Padding Masks

## Learning objective

Extract fixed-horizon action windows from one episode while marking right-padding and preserving requested start order.

## Paper connection and scope

ACT motivates predicting future action chunks. This exercise only builds supervised target windows from one recorded episode. Zero right-padding and True=valid masks are explicit educational conventions; no CVAE, policy inference, or cross-episode concatenation is implemented.

Source sections: SectionIV.A: Action Chunking and Temporal Ensemble; action-sequence prediction; SectionIV.B: demonstration chunks used by the conditional VAE.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Add horizon offsets to each requested start to form a source-index grid. Its comparison with episode length is the validity mask. Gather only safe indices and explicitly replace padded targets with zero. Preserve row order and keep the mask independent of action values. Time and output memory are O(SHD), plus O(TD+S) validation.

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
