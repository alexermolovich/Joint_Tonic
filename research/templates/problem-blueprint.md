---
schema_version: 1
problem_id: "stable-problem-slug"
content_version: "0.1.0"
status: "idea | drafted | reviewed | implemented | published | retired"
title: "Problem title"
summary: "One-sentence learner-facing summary."
type: "function | component | debug | pipeline | optimization | experiment | incident"
difficulty: "easy | medium | hard | research"
estimated_minutes: 30
domains:
  - "perception"
topics:
  - "specific-concept"
paper_ids:
  - "year-short-title"
paper_sections:
  - "Section or figure used to verify the mechanism"
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: "python"
  python: "3.12"
  image_digest: "sha256:todo"
  dependencies:
    numpy: "2.1.*"
  limits:
    wall_seconds: 3
    cpu_seconds: 2
    memory_mb: 512
    output_kb: 64
entrypoint: "solution.function_name"
physical_contract:
  frames: []
  units: {}
  axes: "not-applicable"
  timestamp_assumptions: "not-applicable"
  batching: "Describe batch dimensions and padding/masking."
grading:
  mode: "exact | numerical | metric-threshold | performance | rubric"
  seed: 20261113
  rtol: 1.0e-6
  atol: 1.0e-7
  public_case_families: []
  hidden_case_families: []
  performance_class: "none"
fixtures:
  source: "synthetic"
  license: "CC0-1.0"
  version_or_hash: "todo"
provenance:
  authoring_notes: "Original exercise derived from the cited mechanism."
  primary_urls: []
  implementation_urls: []
owners: []
reviewers: []
---

# Problem title

## Learning objective

State one observable capability the learner will gain.

## Paper connection and scope

Identify the paper mechanism and exact section/figure/equation used for verification. State clearly what the exercise simplifies and why passing it does not imply full paper reproduction.

## Contract

### Inputs

Document every argument with shape, dtype, valid range, units, coordinate frame, timestamp semantics, and device behavior where applicable.

### Outputs

Document shape, dtype, order, units, frame, numerical range, and mutation/aliasing behavior.

### Errors and edge cases

List supported minimal/empty cases and inputs that must raise a documented error.

## Learner prompt draft

Write concise original problem copy. Include enough theory to make the task self-contained without reproducing paper prose.

## Worked examples

Provide at least two small examples with explanations. Avoid leaking hidden cases.

## Starter-code plan

- Files and entry point.
- Types/signatures supplied.
- TODO boundaries.

## Reference-solution plan

- Algorithm and complexity.
- Numerical/stability considerations.
- Permitted implementation alternatives.

## Evaluator plan

| Case family | Public/hidden | Invariant or metric | Tolerance/threshold | Why it matters |
|---|---|---|---|---|
| Nominal | Public | Expected behavior | Declared above | Teaches contract |
| Edge | Hidden | Robustness invariant | Declared above | Prevents overfitting |

Describe determinism controls, flaky-test risks, calibrated performance hardware if any, and how platform failures are separated from learner failures.

## Visualization plan

Specify a safe bounded visualization adapter or write `none`. Include a text/table fallback.

## Theory and hints

- Theory outline.
- Progressive hint 1.
- Progressive hint 2.
- Common failure modes.

## MLOps/reproducibility extension

Connect the mechanism to at least one of dataset validation/lineage, experiment reproducibility, packaging, edge inference, deployment, monitoring, drift, rollback, or safety. If not appropriate, explain why.

## Editorial checklist

- [ ] Metadata and paper IDs resolve.
- [ ] Shapes, frames, units, axes, time, and batching are explicit.
- [ ] Prompt and explanation are original.
- [ ] Fixture source/license is verified.
- [ ] Reference solution passes public and hidden tests.
- [ ] Hidden tests cover documented behavior only.
- [ ] Runtime/dependencies are pinned.
- [ ] Accessibility and visualization fallback are reviewed.
- [ ] Paper deviation and reproduction limits are honest.
- [ ] Subject-matter and evaluator reviewers approved.
