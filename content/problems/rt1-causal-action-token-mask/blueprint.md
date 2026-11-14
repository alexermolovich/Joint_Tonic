---
schema_version: 1
problem_id: rt1-causal-action-token-mask
content_version: 1.0.0
status: implemented
title: Build a Causal Action-Token Mask
summary: >-
  Construct RT-1’s reference causal mask while preventing direct action-slot
  attention to action slots.
type: component
difficulty: medium
estimated_minutes: 35
domains:
  - VLA and embodied robot learning
topics:
  - rt1
  - causal-attention
  - action-token-layout
paper_ids:
  - 2022-rt-1
paper_sections:
  - 'RT-1 Section5.1: Loss and causal masking'
  - >-
    TransformerNetwork._generate_masks and _assemble_input_token_sequence at
    commit 4569641b8111f3f402c32d8e24becd2a6e952ecc
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
entrypoint: solution.rt1_attention_mask
physical_contract:
  frames:
    - 'Not applicable: token positions, not spatial coordinates'
  units:
    positions: integer token indices
    mask: boolean allowed-attention relation
  axes: >-
    Rows=query positions; columns=key positions. Each timestep stores V visual
    slots then A action slots.
  timestamp_assumptions: >-
    Timesteps are ordered oldest to newest at a fixed caller-controlled period;
    no timestamp values enter the mask.
  batching: >-
    One(L,L) mask shared by examples with the same fixed layout; no padding or
    batch dimension in this component.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - one timestep with two visual and two action slots
    - two timesteps with one visual and one action slot
  hidden_case_families:
    - multi-timestep layouts
    - query-key orientation
    - action diagonal exclusion
    - visual access to prior action placeholders
    - integer and size validation
  performance_class: 'none; resource budget only, no latency ranking'
fixtures:
  source: Original deterministic synthetic examples and evaluator cases
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    This exercise reproduces the structural mask in the pinned official RT-1
    implementation using a NumPy boolean output. It omits token embedding,
    shifted prediction readouts, sequence padding, and the transformer. The
    reference implementation zeroes input action embeddings; this mask alone is
    not a license to insert teacher-forced action labels.
  primary_urls:
    - 'https://arxiv.org/abs/2212.06817'
  implementation_urls:
    - >-
      https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/transformer_network.py#L161-L196
    - >-
      https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/transformer_network.py#L585-L600
owners:
  - Joint Tonic content
reviewers:
  - code_issue_scout
review_status:
  author: draft authored; verification recorded in review.md
  independent_subject_matter: approved by code_issue_scout
  independent_evaluator: contract approved by code_issue_scout; implementation pending
evaluator_sha256: 3a38165e5537f3c6f2343f0ff69df4245128cec8721bb0d54c054839bcb81b29
---

# Build a Causal Action-Token Mask

## Learning objective

Construct RT-1’s reference causal mask while preventing direct action-slot attention to action slots.

## Paper connection and scope

This exercise reproduces the structural mask in the pinned official RT-1 implementation using a NumPy boolean output. It omits token embedding, shifted prediction readouts, sequence padding, and the transformer. The reference implementation zeroes input action embeddings; this mask alone is not a license to insert teacher-forced action labels.

Source sections: RT-1 Section5.1: Loss and causal masking; TransformerNetwork._generate_masks and _assemble_input_token_sequence at commit 4569641b8111f3f402c32d8e24becd2a6e952ecc.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Create token indices and identify action slots using the index remainder within a timestep. A broadcast comparison gives the causal lower triangle. Remove only pairs whose query and key are both action slots. Visual rows may still see earlier action placeholders, matching the documented source behavior. Time and result memory are O(L²).

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
