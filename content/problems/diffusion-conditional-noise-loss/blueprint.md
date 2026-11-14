---
schema_version: 1
problem_id: diffusion-conditional-noise-loss
content_version: 1.0.0
status: implemented
title: Compute a Conditional Noise-Prediction Loss
summary: >-
  Reduce predicted-versus-supplied diffusion noise errors over exactly the valid
  action scalars while preserving training gradients.
type: component
difficulty: medium
estimated_minutes: 30
domains:
  - VLA and embodied robot learning
topics:
  - diffusion-policy
  - noise-prediction
  - masked-loss
paper_ids:
  - 2023-diffusion-policy
paper_sections:
  - 'SectionIII: conditional denoising diffusion training objective'
  - >-
    Joint Tonic published diffusion-action-noising contract supplies target
    noise and validity masks
track_ids: []
prerequisite_problem_ids:
  - diffusion-action-noising
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
    torch: 2.6.0+cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
entrypoint: solution.conditional_noise_loss
physical_contract:
  frames:
    - >-
      Normalized action coordinates associated with the caller’s controller
      schema; no coordinate conversion
  units:
    prediction: dimensionless noise in normalized action space
    target_noise: dimensionless supplied corruption noise
    loss: mean squared normalized-noise error
  axes: 'prediction and target_noise(B,H,D); valid(B,H); output is a scalar tensor'
  timestamp_assumptions: >-
    H is a future control horizon; diffusion level and observation context
    already condition the upstream prediction and are not function arguments.
  batching: >-
    One global mean over all valid scalar channels across B and H; not an
    equal-weight mean of per-item losses.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - masked two-channel prediction
    - unequal valid horizons across two batch items
  hidden_case_families:
    - all-padding rejection
    - gradient scaling and masked gradients
    - noncontiguous tensors
    - dtype/device/value errors
    - target gradients preserved
  performance_class: 'none; resource budget only, no latency ranking'
fixtures:
  source: Original deterministic synthetic examples and evaluator cases
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    This component computes the masked noise-regression reduction after a
    conditional denoiser has run. It does not build that network, sample
    timesteps/noise, construct noised actions, or duplicate the published
    forward-noising problem. Validity masking and the exact global reduction are
    explicit teaching contracts.
  primary_urls:
    - 'https://arxiv.org/abs/2303.04137'
  implementation_urls: []
owners:
  - Joint Tonic content
reviewers:
  - code_issue_scout
review_status:
  author: draft authored; verification recorded in review.md
  independent_subject_matter: approved by code_issue_scout
  independent_evaluator: contract approved by code_issue_scout; implementation pending
evaluator_sha256: bcff441428fa17b732c45ebe67830990ed498dafe7ce38a4c54061e4488a20e9
---

# Compute a Conditional Noise-Prediction Loss

## Learning objective

Reduce predicted-versus-supplied diffusion noise errors over exactly the valid action scalars while preserving training gradients.

## Paper connection and scope

This component computes the masked noise-regression reduction after a conditional denoiser has run. It does not build that network, sample timesteps/noise, construct noised actions, or duplicate the published forward-noising problem. Validity masking and the exact global reduction are explicit teaching contracts.

Source sections: SectionIII: conditional denoising diffusion training objective; Joint Tonic published diffusion-action-noising contract supplies target noise and validity masks.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Subtract the supplied target noise from the prediction, square the residual, and apply the timestep mask across all D channels. Divide the total by the number of valid scalar targets, D times valid.sum(). Keep the calculation in tensors so gradients reach both floating inputs. The contract bounds keep this sum finite in float32. Time and temporary storage are O(BHD).

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
