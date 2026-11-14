---
schema_version: 1
problem_id: palm-e-project-sensor-features
content_version: 1.0.0
status: implemented
title: Project Continuous Sensor Features into Language Width
summary: Isolate a supplied affine projection into a language embedding width.
type: component
difficulty: easy
estimated_minutes: 35
domains:
  - VLA and embodied robot learning
topics:
  - 2023-palm-e
  - policy-components
paper_ids:
  - 2023-palm-e
paper_sections:
  - 'Sections3–4: continuous sensor embeddings'
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: python
  python: 3.12.3
  image_digest: pending-local-worker-build
  dependencies:
    numpy: 2.2.4
    torch: 2.6.0+cpu
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
entrypoint: solution.project_sensor_features
physical_contract:
  frames:
    - As specified in the typed contract; no implicit frame conversion
  units:
    actions: caller-declared normalized Euclidean action channels
    embeddings: dimensionless
    time: 'fixed control ticks, not flow time'
  axes: >-
    B=independent observations,N=sensor token positions,C=sensor
    width,E=language width
  timestamp_assumptions: One aligned observation per batch item; temporal calibration is upstream.
  batching: 'features(B,N,C), weight(C,E), bias(E), valid(B,N), output(B,N,E)'
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - two-worked-examples
  hidden_case_families:
    - shape-dtype-validation
    - masked-behavior
    - boundaries
    - noncontiguous-and-immutability
    - gradients-where-declared
    - realistic-scale
fixtures:
  source: Original deterministic synthetic examples and evaluator cases
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Isolate a supplied affine projection into a language embedding width. PaLM-E
    permits richer modality encoders; this exercise does not assert every
    encoder is one affine layer. Inputs are already normalized modality
    features, not raw heterogeneous physical units.
  primary_urls:
    - 'https://arxiv.org/abs/2303.03378'
  implementation_urls: []
owners:
  - vla_implementation
reviewers:
  - code_issue_scout
evaluator_sha256: 5c5903bc806668ce4d1e9e9cea7bae77344eaf19609365f7d67b8fb86c306479
---

# Project Continuous Sensor Features into Language Width

## Learning objective

Isolate a supplied affine projection into a language embedding width.

## Paper connection and scope

Isolate a supplied affine projection into a language embedding width. PaLM-E permits richer modality encoders; this exercise does not assert every encoder is one affine layer. Inputs are already normalized modality features, not raw heterogeneous physical units.

Source sections: Sections3–4: continuous sensor embeddings.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Multiply each sensor feature row by the supplied projection matrix, then add the bias and zero invalid rows. Masking after the bias prevents missing tokens from receiving a bias-only embedding or contributing to its gradient. The operation preserves token positions and changes only feature width. Time is O(BNCE), output storage O(BNE).

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
