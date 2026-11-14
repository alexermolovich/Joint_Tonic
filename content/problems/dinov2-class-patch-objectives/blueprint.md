---
schema_version: 1
problem_id: dinov2-class-patch-objectives
content_version: 1.0.0
status: implemented
title: Combine Class-Token and Masked-Patch Objectives
summary: Combine Class-Token and Masked-Patch Objectives
type: function
difficulty: hard
estimated_minutes: 40
domains:
  - perception
topics:
  - dinov2
  - paper-component
paper_ids:
  - 2023-dinov2
paper_sections:
  - Mechanism and explicit teaching conventions in theory.md
track_ids: []
prerequisite_problem_ids:
  - dinov2-center-sharpen
runtime:
  language: python
  python: 3.12.3
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  dependencies:
    torch: 2.6.0+cpu
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.class_patch_loss
physical_contract:
  frames:
    - Explicit caller grid/view frames in statement
  units:
    features: dimensionless; BEV geometry in metres where stated
  axes: >-
    student_class(B,V,K), teacher_class(B,2,K),
    student_patch/teacher_patch(B,P,K), mask(B,P); scalar output.
  timestamp_assumptions: One explicitly paired batch; no internal clock.
  batching: >-
    student_class(B,V,K), teacher_class(B,2,K),
    student_patch/teacher_patch(B,P,K), mask(B,P); scalar output.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - worked-examples
    - minimal-shape
  hidden_case_families:
    - validation
    - edge-policy
    - layout
    - preservation
    - independent-oracle
    - scale
  performance_class: cpu
  evaluator_sha256: b3b6ce1df42cb26b5dd4e28d5b3930bfb7b5486c09ef2d814edd7c5700b81683
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original bounded teaching task; variants explicitly distinguished from full
    paper systems.
  primary_urls:
    - 'https://arxiv.org/abs/2304.07193'
  implementation_urls: []
  paper_card: research/papers/vision-vlm-3d/2023-dinov2.md
  manifest: research/manifests/vision-vlm-3d.md
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Combine Class-Token and Masked-Patch Objectives

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/dinov2-class-patch-objectives. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate all teacher rows, then detach the supplied targets. Use stable student log-softmax at the supplied temperature. Average class cross-entropy over all images and permitted teacher/student view pairs. Separately average patch cross-entropy over selected positions across the batch. The empty selection contributes student_patch.sum()*0 so backward remains defined. Combine with the supplied weights; no teacher gradients or target renormalization is introduced. Work and storage are O(B(V+P)K).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox dinov2-class-patch-objectives. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
