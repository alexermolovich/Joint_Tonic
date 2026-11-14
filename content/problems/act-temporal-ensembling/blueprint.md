---
schema_version: 1
problem_id: act-temporal-ensembling
content_version: 1.0.0
status: implemented
title: Blend Overlapping Action Chunks with Temporal Ensembling
summary: >-
  Align predictions to one target control tick and combine eligible chunks with
  ACT’s oldest-first exponential weighting.
type: component
difficulty: medium
estimated_minutes: 45
domains:
  - VLA and embodied robot learning
topics:
  - act
  - temporal-ensembling
  - action-alignment
paper_ids:
  - 2023-aloha-act
paper_sections:
  - 'SectionIV.A: exponential temporal ensemble, w0 is the oldest action'
  - 'SectionVI.A: action chunking and temporal ensembling ablation'
track_ids: []
prerequisite_problem_ids: []
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
entrypoint: solution.temporal_ensemble
physical_contract:
  frames:
    - All chunks share one caller-declared action frame and channel schema
  units:
    predictions: per-channel normalized Euclidean action values
    start_ticks: integer control ticks
    target_tick: integer control tick
    decay: dimensionless weight decay per eligible prediction rank
  axes: 'predictions(C,H,D), valid(C,H), start_ticks(C), output(D), weights(C)'
  timestamp_assumptions: >-
    Strictly increasing chunk start ticks, fixed control period, horizon offset
    h predicts start_tick+h. Only chunks available no later than target_tick are
    eligible.
  batching: >-
    C indexes overlapping chunk predictions for one robot episode, not
    independent robots. D channels are averaged independently.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - three aligned predictions with geometric weights
    - zero-valued valid prediction and mean weighting
  hidden_case_families:
    - masked candidates and rank compression
    - target outside all chunks
    - future chunks
    - nonconsecutive start ticks
    - large decay
    - dtype/shape/value errors
  performance_class: 'none; resource budget only, no latency ranking'
fixtures:
  source: Original deterministic synthetic examples and evaluator cases
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    This exercise implements ACT’s temporal ensembling after chunk predictions
    already exist. It follows the primary paper’s oldest-first rank convention.
    Explicit validity masks, nonconsecutive start ticks, and returned diagnostic
    weights are teaching extensions; normalized Euclidean channels exclude
    quaternion averaging and wrapped-angle interpolation.
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
evaluator_sha256: 89ef336110af84e627610c9c6998d523e21c3d09f207fd13e9f039a64eaca5cb
---

# Blend Overlapping Action Chunks with Temporal Ensembling

## Learning objective

Align predictions to one target control tick and combine eligible chunks with ACT’s oldest-first exponential weighting.

## Paper connection and scope

This exercise implements ACT’s temporal ensembling after chunk predictions already exist. It follows the primary paper’s oldest-first rank convention. Explicit validity masks, nonconsecutive start ticks, and returned diagnostic weights are teaching extensions; normalized Euclidean channels exclude quaternion averaging and wrapped-angle interpolation.

Source sections: SectionIV.A: exponential temporal ensemble, w0 is the oldest action; SectionVI.A: action chunking and temporal ensembling ablation.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Compute each chunk's offset to the target tick, then select only in-range, valid predictions. Their existing chronological order defines compact ranks; gaps do not change rank spacing. Exponentiate negative decay times these ranks in float64, normalize, and blend selected vectors. Cast both diagnostic weights and action back to the input dtype. Zero-valued actions remain eligible. Input validation is O(CHD), blending O(CD).

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
