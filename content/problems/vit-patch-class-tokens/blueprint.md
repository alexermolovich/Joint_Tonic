---
schema_version: 1
problem_id: vit-patch-class-tokens
content_version: 1.0.0
status: implemented
title: Build Learned Patch and Class Tokens
summary: Build Learned Patch and Class Tokens
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - perception
topics:
  - vision-transformer
  - paper-component
paper_ids:
  - 2021-vision-transformer
paper_sections:
  - Mechanism and scope defined in theory.md
track_ids: []
prerequisite_problem_ids:
  - vit-patchify-reconstruct
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  dependencies:
    torch: 2.6.0+cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.build_vit_tokens
physical_contract:
  frames:
    - Declared explicitly in learner contract
  units:
    features: dimensionless; image indices in pixels where applicable
  axes: >-
    patches(B,N,F), projection(F,D), bias(D), cls(D), positions(N+1,D);
    result(B,N+1,D).
  timestamp_assumptions: Same upstream observation or training snapshot; no timestamp input.
  batching: >-
    patches(B,N,F), projection(F,D), bias(D), cls(D), positions(N+1,D);
    result(B,N+1,D).
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.e-7
  atol: 1.e-9
  public_case_families:
    - worked-examples
    - minimal-shape
  hidden_case_families:
    - validation
    - empty-policy
    - noncontiguous
    - immutability
    - deterministic-order
    - realistic-batch
  performance_class: none
  evaluator_sha256: adda8c153c523e0a447bfb69679b46a4dc27877effe40313e29934602dd1d9ba
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original teaching contract and synthetic fixtures, no copied paper
    prose/figures/code.
  primary_urls:
    - 'https://arxiv.org/abs/2010.11929'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Build Learned Patch and Class Tokens

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/vit-patch-class-tokens. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate ranks and all dimensions before broadcasting. Multiply patches by the shared projection, add patch bias, expand the class token across B, concatenate it before the patch rows, and add all N+1 positions. Keep normal PyTorch operations to preserve gradients to every input, including shared parameters. Complexity is O(BNFD) for projection plus O(BND) storage. The class token bypasses the patch affine transform.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox vit-patch-class-tokens. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
