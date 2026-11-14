---
schema_version: 1
problem_id: rt1-compact-visual-tokens
content_version: 1.0.0
status: implemented
title: Select Compact Visual Tokens with Learned Attention
summary: >-
  Turn supplied learned spatial logits into normalized attention maps and
  compress visual features without mixing examples.
type: component
difficulty: medium
estimated_minutes: 40
domains:
  - VLA and embodied robot learning
topics:
  - rt1
  - visual-token-compression
  - masked-attention
paper_ids:
  - 2022-rt-1
paper_sections:
  - 'RT-1 Section5.1: Image and language tokenization; TokenLearner'
  - >-
    Official TokenLearnerModule.call at commit
    4569641b8111f3f402c32d8e24becd2a6e952ecc
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
    torch: 2.6.0+cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
entrypoint: solution.compact_visual_tokens
physical_contract:
  frames:
    - Image-grid feature locations; no metric coordinate transform
  units:
    features: dimensionless learned features
    logits: dimensionless log scores
    weights: dimensionless normalized weights
  axes: >-
    B=batch, N=flattened row-major image locations, C=feature channels, K=output
    tokens
  timestamp_assumptions: >-
    Each batch item is one synchronized image feature map; independent frames
    may be folded into B by the caller.
  batching: >-
    features(B,N,C), logits(B,K,N), optional valid(B,N); independent
    normalization for every (b,k).
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - two weighted tokens with a masked location
    - two independent single-location images
  hidden_case_families:
    - stable logits
    - mixed masks
    - noncontiguous tensors
    - gradients
    - all-masked image rejection
    - dtype/device/shape/value validation
  performance_class: 'none; resource budget only, no latency ranking'
fixtures:
  source: Original deterministic synthetic examples and evaluator cases
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    This exercise isolates the spatial softmax and weighted aggregation in
    RT-1’s TokenLearner. Logits are supplied; learning their LayerNorm/MLP
    generator, image encoding, language conditioning, and policy training are
    out of scope. The optional padding mask is an original batching extension.
  primary_urls:
    - 'https://arxiv.org/abs/2212.06817'
  implementation_urls:
    - >-
      https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/tokenizers/token_learner.py#L103-L117
owners:
  - Joint Tonic content
reviewers:
  - code_issue_scout
review_status:
  author: draft authored; verification recorded in review.md
  independent_subject_matter: approved by code_issue_scout
  independent_evaluator: contract approved by code_issue_scout; implementation pending
evaluator_sha256: d1087e966c5b7d48f9a54163cd09fc3deb87316e1bb77f83e892c3a571fe902b
---

# Select Compact Visual Tokens with Learned Attention

## Learning objective

Turn supplied learned spatial logits into normalized attention maps and compress visual features without mixing examples.

## Paper connection and scope

This exercise isolates the spatial softmax and weighted aggregation in RT-1’s TokenLearner. Logits are supplied; learning their LayerNorm/MLP generator, image encoding, language conditioning, and policy training are out of scope. The optional padding mask is an original batching extension.

Source sections: RT-1 Section5.1: Image and language tokenization; TokenLearner; Official TokenLearnerModule.call at commit 4569641b8111f3f402c32d8e24becd2a6e952ecc.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Validate every tensor before masking. Apply softmax along the spatial axis after replacing invalid logits with negative infinity, then multiply the attention weights by the feature matrix. Because no tensor is detached, gradients reach both the feature extractor and the attention-logit generator. Time is O(BKNC); auxiliary/output storage is O(BK(N+C)).

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
