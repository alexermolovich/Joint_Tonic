---
schema_version: 1
problem_id: clip-prompt-ensemble
content_version: 1.0.0
status: implemented
title: Build a Prompt-Ensembled Zero-Shot Classifier
summary: Build a Prompt-Ensembled Zero-Shot Classifier
type: function
difficulty: medium
estimated_minutes: 35
domains:
  - perception
topics:
  - clip
  - paper-component
paper_ids:
  - 2021-clip
paper_sections:
  - Mechanism and conventions defined in theory.md
track_ids: []
prerequisite_problem_ids:
  - clip-normalize-embeddings
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; local bubblewrap baseline
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  budget_status: actual shared worker caps; per-process address-space limit
entrypoint: solution.prompt_ensemble_classifier
physical_contract:
  frames:
    - Explicit caller-observation conventions in statement
  units:
    features: dimensionless
  axes: 'images(B,D),prompts(C,P,D); logits(B,C),prototypes(C,D).'
  timestamp_assumptions: One observation batch; no internal clock.
  batching: 'images(B,D),prompts(C,P,D); logits(B,C),prototypes(C,D).'
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
  evaluator_sha256: 69a35ba239f407b592c48c9901990a0caae00b7690b08e84be2bf57d460f3877
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original bounded teaching task. No copied source code or figure.
  primary_urls:
    - 'https://arxiv.org/abs/2103.00020'
  implementation_urls: []
  paper_card: research/papers/vision-vlm-3d/2021-clip.md
  manifest: research/manifests/vision-vlm-3d.md
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---
# Build a Prompt-Ensembled Zero-Shot Classifier

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/clip-prompt-ensemble. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate each image and prompt norm. Normalize prompts independently along D, average them only within their class, reject a nearly cancelling class mean, and normalize the mean again. Normalize image rows and compute their dot products with class prototypes divided by positive temperature. Returning logits preserves score ordering without an unnecessary softmax. Prototype construction costs O(CPD), and scoring costs O(BCD).

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox clip-prompt-ensemble. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
