---
schema_version: 1
problem_id: act-cvae-loss
content_version: 1.0.0
status: implemented
title: Compute a Masked CVAE Reconstruction and KL Loss
summary: Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective.
type: component
difficulty: medium
estimated_minutes: 35
domains:
  - VLA and embodied robot learning
topics:
  - 2023-aloha-act
  - policy-components
paper_ids:
  - 2023-aloha-act
paper_sections:
  - 'Section IV-B: Modeling human data'
track_ids: []
prerequisite_problem_ids:
  - act-sliding-action-chunks
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
entrypoint: solution.cvae_loss
physical_contract:
  frames:
    - As specified in the typed contract; no implicit frame conversion
  units:
    actions: caller-declared normalized Euclidean action channels
    embeddings: dimensionless
    time: 'fixed control ticks, not flow time'
  axes: >-
    B=batch,H=future control ticks,D=normalized Euclidean action
    channels,Z=latent coordinates
  timestamp_assumptions: One aligned observation per batch item; temporal calibration is upstream.
  batching: >-
    prediction/target(B,H,D), valid(B,H), mean/log_variance(B,Z), three scalar
    outputs
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
    Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective. The
    global valid-scalar reconstruction mean and batch-mean latent sum are
    explicit teaching reductions. No encoder, latent sampling, transformer, or
    training run is reproduced.
  primary_urls:
    - 'https://arxiv.org/abs/2304.13705'
  implementation_urls: []
owners:
  - vla_implementation
reviewers:
  - code_issue_scout
evaluator_sha256: fed527d71e8fcb93388a3197231025baab08c2e0fc6a5a2e9c3b25de7dfd9534
---

# Compute a Masked CVAE Reconstruction and KL Loss

## Learning objective

Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective.

## Paper connection and scope

Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective. The global valid-scalar reconstruction mean and batch-mean latent sum are explicit teaching reductions. No encoder, latent sampling, transformer, or training run is reproduced.

Source sections: Section IV-B: Modeling human data.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Reduce the masked absolute action residual over valid scalar targets. Independently sum diagonal-Gaussian KL terms over latent dimensions and average over all batch items. Combine the two scalars with beta, preserving gradients through actions, targets and posterior parameters. The two terms have deliberately different denominators. Time and temporary storage are O(BHD+BZ).

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
