---
schema_version: 1
problem_id: diffusion-receding-horizon-window
content_version: 1.0.0
status: implemented
title: Execute a Receding-Horizon Action Window
summary: >-
  Extract the controller-supported prefix of a predicted future trajectory after
  a specified alignment offset.
type: component
difficulty: easy
estimated_minutes: 35
domains:
  - VLA and embodied robot learning
topics:
  - 2023-diffusion-policy
  - policy-components
paper_ids:
  - 2023-diffusion-policy
paper_sections:
  - 'SectionIII: receding-horizon control'
track_ids: []
prerequisite_problem_ids:
  - act-sliding-action-chunks
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
entrypoint: solution.receding_horizon_window
physical_contract:
  frames:
    - As specified in the typed contract; no implicit frame conversion
  units:
    actions: caller-declared normalized Euclidean action channels
    embeddings: dimensionless
    time: 'fixed control ticks, not flow time'
  axes: >-
    B=independent observations,H=future control ticks,D=unchanged actuator
    channels
  timestamp_assumptions: One aligned observation per batch item; temporal calibration is upstream.
  batching: 'trajectory(B,H,D), valid(B,H), output(B,execute_steps,D)'
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
    Extract the controller-supported prefix of a predicted future trajectory
    after a specified alignment offset. This returns a command buffer for a
    synthetic controller; it does not drive a robot, run denoising or infer the
    observation-horizon offset.
  primary_urls:
    - 'https://arxiv.org/abs/2303.04137'
  implementation_urls: []
owners:
  - vla_implementation
reviewers:
  - code_issue_scout
evaluator_sha256: f582193dccf59a499f57211a8ab0b4063720508c5e0513a949c5ef94187cf9f7
---

# Execute a Receding-Horizon Action Window

## Learning objective

Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset.

## Paper connection and scope

Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset. This returns a command buffer for a synthetic controller; it does not drive a robot, run denoising or infer the observation-horizon offset.

Source sections: SectionIII: receding-horizon control.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Validate the requested offset and length, require every selected validity entry to be true, and return a copy of the corresponding trajectory slice. Do not remove holes or invent a substitute action. Full input validation costs O(BHD); copying the selected buffer costs O(BKD) for K execution steps.

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
