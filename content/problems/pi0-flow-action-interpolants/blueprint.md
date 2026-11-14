---
schema_version: 1
problem_id: pi0-flow-action-interpolants
content_version: 1.0.0
status: implemented
title: Sample Flow-Matching Action Interpolants and Targets
summary: >-
  Construct pi0-style noise-to-action linear interpolants and constant velocity
  targets from supplied noise, times, and validity masks.
type: component
difficulty: medium
estimated_minutes: 35
domains:
  - VLA and embodied robot learning
topics:
  - pi0
  - flow-matching
  - continuous-actions
paper_ids:
  - 2024-pi0
paper_sections:
  - >-
    arXiv2410.24164v4 SectionIV page5: noised actionsA_tau=tau*A+(1-tau)*noise
    and targetA-noise
  - 'SectionIV: forward Euler integration fromtau=0 to1'
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
entrypoint: solution.flow_action_interpolants
physical_contract:
  frames:
    - Normalized Euclidean action channels in one caller-declared control frame
  units:
    actions: dimensionless normalized action coordinates
    noise: dimensionless supplied samples in the same coordinates
    tau: 'dimensionless flow time in[0,1]'
    target_velocity: normalized action coordinate change per unit flow time
  axes: 'actions and noise(B,H,D); tau(B); valid(B,H); both outputs(B,H,D)'
  timestamp_assumptions: >-
    H indexes future physical control ticks; tau is generative flow time and
    never a robot timestamp.
  batching: >-
    Each batch item has one flow time broadcast across its horizon and action
    channels. Masking zeros both outputs at invalid horizon positions.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0.000001
  atol: 1.e-7
  public_case_families:
    - fractional interpolation with two action channels
    - different endpoint times in one batch
  hidden_case_families:
    - all-padding construction
    - gradient identities
    - noncontiguous tensors
    - per-item broadcasting
    - range/dtype/device validation
  performance_class: 'none; resource budget only, no latency ranking'
fixtures:
  source: Original deterministic synthetic examples and evaluator cases
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    The task constructs training samples for the linear interpolation path in
    pi0 arXiv2410.24164v4 SectionIV page5, whose velocity target is
    actions-minus-noise. Earlier v1 printed the opposite sign; this exercise
    pins the corrected v4 equation. Noise and flow times are supplied. Padding
    masks are an educational extension; no full VLA reproduction is claimed.
  primary_urls:
    - 'https://arxiv.org/pdf/2410.24164v4'
  implementation_urls: []
owners:
  - Joint Tonic content
reviewers:
  - code_issue_scout
review_status:
  author: draft authored; verification recorded in review.md
  independent_subject_matter: approved by code_issue_scout
  independent_evaluator: contract approved by code_issue_scout; implementation pending
evaluator_sha256: ecaa07e4952953ce432a494e12146d72cb8c21c00028fa60983469cab975d5bb
---

# Sample Flow-Matching Action Interpolants and Targets

## Learning objective

Construct pi0-style noise-to-action linear interpolants and constant velocity targets from supplied noise, times, and validity masks.

## Paper connection and scope

The task constructs training samples for the linear interpolation path in pi0 arXiv2410.24164v4 SectionIV page5, whose velocity target is actions-minus-noise. Earlier v1 printed the opposite sign; this exercise pins the corrected v4 equation. Noise and flow times are supplied. Padding masks are an educational extension; no full VLA reproduction is claimed.

Source sections: arXiv2410.24164v4 SectionIV page5: noised actionsA_tau=tau*A+(1-tau)*noise and targetA-noise; SectionIV: forward Euler integration fromtau=0 to1.

## Contract

The normative typed function, shapes, physical conventions, errors and examples are in [problem.md](problem.md). Original math and visual traces are in [theory.md](theory.md).

## Implementation

Reshape the per-example flow times to (B,1,1), interpolate linearly between supplied noise and normalized actions, and compute the constant path derivative actions minus noise. Apply the timestep mask to both outputs. Tensor operations preserve gradients through actions, noise and flow time; no random draw or diffusion schedule belongs here. Time and output memory are O(BHD).

The starter, reference, public/hidden evaluator, hints and solution are included in this directory. Fixtures are original synthetic CC0-1.0 data. The reference is checked with the same isolated local Run and Submit paths used by the workspace; the declared limits are the actual shared worker limits. The local OCI image digest is pending and is not represented by the evaluator source hash.

## Verification and review

The independent source/contract review is retained in [review.md](review.md). Runtime verification results are appended there after checks. The hidden suite exercises the documented boundaries, masks, dtype/device, fresh storage and gradients where required. No trained model, external dataset or paper headline result is reproduced.
