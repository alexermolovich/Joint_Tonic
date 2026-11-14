---
schema_version: 1
problem_id: dinov2-teacher-ema
content_version: 1.0.0
status: implemented
title: Update a Teacher Encoder with Exponential Moving Average
summary: >-
  Produce a detached teacher-parameter snapshot from matched teacher/student
  names and one EMA momentum.
type: function
difficulty: easy
estimated_minutes: 30
domains:
  - perception
topics:
  - self-supervised-learning
  - teacher-student
  - exponential-moving-average
paper_ids:
  - 2023-dinov2
paper_sections:
  - >-
    Section 3: discriminative self-supervised pre-training; teacher-student
    update
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  platform: linux-x86_64-cpu
  dependencies:
    torch: 2.6.0
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.update_teacher_ema
physical_contract:
  frames:
    - 'model parameter space, not a geometric frame'
  units:
    parameters: model-dependent numerical values
    momentum: dimensionless
  axes: >-
    Parameter names determine correspondence; each tensor keeps its own shape
    and dtype.
  timestamp_assumptions: >-
    No timestamp input; any temporal or scene alignment is an upstream caller
    responsibility.
  batching: >-
    One optimizer-step boundary per call; no sample batch axis or implicit time
    integration.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - named parameters in different orders
    - momentum zero and one
    - two sequential teacher updates
  hidden_case_families:
    - same-shaped parameters with different key order
    - scalar and empty parameter tensors
    - key/shape/dtype and integer-buffer rejection
    - requires-grad inputs with detached independent outputs
    - empty dictionaries
  performance_class: none
  evaluator_sha256: 7ef67611a7846e21629a4b099ee3fcd285dd1aaa0ee06560d93218fd540f767c
fixtures:
  source: >-
    original synthetic examples in examples.md; future generated fixtures use
    declared seed
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original bounded teaching contract and explanations; source mechanisms
    checked against the paired paper card and primary sources; no paper figures
    or implementation code copied.
  primary_urls:
    - 'https://arxiv.org/abs/2304.07193'
  implementation_urls:
    - >-
      https://github.com/facebookresearch/dinov2/blob/main/dinov2/train/ssl_meta_arch.py
owners:
  - ui_issue_scout
reviewers:
  - paper_explanations
---
# Update a Teacher Encoder with Exponential Moving Average

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/dinov2-teacher-ema. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate dictionaries by name, including all tensors before producing output. Iterate in teacher insertion order and compute momentum*teacher+(1-momentum)*student under torch.no_grad(). Each arithmetic expression creates an independent snapshot even at the endpoint momenta; do not return an input directly. The returned parameters are detached and do not mutate either model. Time and output storage are linear in total parameter elements. This is not a complete state_dict update: buffers and optimizer states have separate semantics.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox dinov2-teacher-ema. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
