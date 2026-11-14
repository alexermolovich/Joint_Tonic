---
schema_version: 1
problem_id: clip-normalize-embeddings
content_version: 1.0.0
status: implemented
title: Normalize Image and Text Embeddings
summary: >-
  Normalize paired image and text feature rows while preserving the PyTorch
  gradient path.
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - perception
topics:
  - vision-language
  - embeddings
  - cosine-similarity
paper_ids:
  - 2021-clip
paper_sections:
  - 'Section 2.3 and Figure 3: normalized image/text feature comparison'
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
entrypoint: solution.normalize_clip_embeddings
physical_contract:
  frames:
    - 'learned embedding coordinates, not a spatial frame'
  units:
    features: dimensionless
  axes: >-
    B rows are paired samples in preserved order; D columns are embedding
    components.
  timestamp_assumptions: >-
    No timestamp input; any temporal or scene alignment is an upstream caller
    responsibility.
  batching: >-
    Both inputs share nonempty (B,D); no masks, padding, time axis, or
    independent retrieval collection.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - 3-4-5 vectors with signs
    - positive rescaling invariance
    - one-row one-component case
  hidden_case_families:
    - row versus column normalization
    - zero and nonfinite norm rejection
    - noncontiguous equal-shape input
    - analytic first-component gradient and independent storage
  performance_class: none
  evaluator_sha256: 8b68c37b203727ab084d7c33badf5ebbe0de16676dfcb0689b8a921ff51c450f
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
    - 'https://arxiv.org/abs/2103.00020'
  implementation_urls: []
owners:
  - ui_issue_scout
reviewers:
  - paper_explanations
---
# Normalize Image and Text Embeddings

## Reviewed contract

The adjacent problem.md, theory.md, examples.md and hints.md contain the independently reviewed contract and explanation. Source draft: content/planned/perception/clip-normalize-embeddings. Reference, starter and evaluator implement this exact contract.

## Reference strategy

Validate both tensors and compute validation norms in float64, as the contract requires. Divide each original tensor by its own last-axis norm with keepdim=True. The denominator has shape (B,1), so each sample is normalized independently. These ordinary differentiable operations preserve autograd and allocate new outputs. Cost is O(BD) time and output storage. Avoid detach, normalization across B, or adding an undocumented epsilon.

## Publication validation

Run public and hidden suites through apps/worker/check_references.py --sandbox clip-normalize-embeddings. The local baseline has pinned dependencies and the enforced caps above. OCI image digest remains pending; no full-paper reproduction or hosted deployment is claimed.
