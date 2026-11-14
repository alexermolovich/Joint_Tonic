---
schema_version: 1
problem_id: "training-serving-transform-skew"
content_version: "0.1.0"
status: "reviewed"
title: "Detect Training-Serving Transform Skew"
summary: "Locate transformed feature cells that disagree between training and serving beyond declared tolerances."
type: "function"
difficulty: "easy"
estimated_minutes: 25
domains: ["robotics-mlops"]
topics: ["preprocessing-parity","deployment-validation"]
paper_ids: ["2017-tfx-production-ml-platform"]
paper_sections: ["Section 3.2: Data Transformation"]
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: "python"
  python: "3.12.3"
  image_digest: null
  image_status: "pending-build-and-verification"
  dependencies: {numpy: "2.2.4"}
  platform: "linux-x86_64-cpu"
  limits: {wall_seconds: 3, cpu_seconds: 2, memory_mb: 512, output_kb: 64}
  budget_status: "planned; not measured"
entrypoint: "solution.transform_skew"
physical_contract:
  frames: ["Caller-declared identical frame for each matched feature; no coordinate transform is performed."]
  units: {"values":"per-feature physical unit","atol":"same unit as its feature","rtol":"dimensionless"}
  axes: "Rows are aligned observations; columns preserve feature_names order."
  timestamp_assumptions: "Row i on both sides is the same captured observation at the same timestamp; no resampling or clock conversion."
  batching: "Two float64 tensors (N,D), one tolerance vector (D,)."
grading:
  mode: "exact"
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families: ["absolute tolerance equality","relative tolerance with zero reference","empty aligned batch"]
  hidden_case_families: ["shape mismatch without broadcasting","duplicate feature names","NaN/infinity rejection","zero feature columns","negative tolerance","float32 rejection"]
  performance_class: "none; no timing leaderboard"
fixtures:
  source: "original synthetic examples"
  license: "CC0-1.0"
  version_or_hash: "synthetic-mlops-0.1.0"
  generated_fixture_hash: null
provenance:
  authoring_notes: "Original instructional contract, examples, and diagrams; no copied paper code or figures."
  primary_urls: ["https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/"]
  implementation_urls: []
  paper_card: "research/papers/mlops-sim2real/2017-tfx-production-ml-platform.md"
  manifest: "research/manifests/mlops-sim2real.md"
owners: ["code_issue_scout"]
reviewers: ["ui_issue_scout"]
---
# Detect Training-Serving Transform Skew

## Learning objective

Locate transformed feature cells that disagree between training and serving beyond declared tolerances.

## Paper connection and scope

The source motivates shared transformation logic. This aligned-output parity check is an original test component, separate from distribution drift or complete model-bundle verification. Source location: Section 3.2: Data Transformation. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).

## Contract and worked examples

Compare paired float64 feature matrices cell by cell using abs(serve-train) > atol[column] + rtol*abs(train). Return failing (row, feature_name) pairs in row-major order. statement.md is the normative input/error/output specification; examples.md expands its two public examples. Inputs must not be mutated. No published implementation or evaluator exists yet.

## Starter-code plan

Provide the signature and necessary types/imports from statement.md. Leave the component body as the learner's task. No networking, filesystem access, or simulator control belongs in learner code.

## Reference-solution plan

Validate shape, dtype, finiteness, names, and tolerance bounds. Compute a boolean mismatch mask using training as the relative-error reference; enumerate true cells in row-major order. O(ND) time, O(ND) memory for a vectorized implementation.

## Evaluator plan

Public families: absolute tolerance equality; relative tolerance with zero reference; empty aligned batch. Hidden families: shape mismatch without broadcasting; duplicate feature names; NaN/infinity rejection; zero feature columns; negative tolerance; float32 rejection. Compare order, shape, and dtype exactly; apply the stated numerical tolerances where relevant. Validate errors by exception type rather than message. Check input immutability. Seed generated fixtures with 20261113; no wall-clock timing or network enters correctness grading. Report platform setup failures separately from learner failures. Image digest, fixture hashes, implementation, and isolated evaluator checks remain pending.

## Visualization plan

Original paired transform paths and per-cell difference table; static text alternative. This is a Markdown diagram specification, not a claim that today's renderer supports Mermaid. Keep the static text/table fallback usable before publication.

## Theory, hints, and reproducibility

Read theory.md for intuition, defined math, a worked example, robot failure modes, and conceptual questions. hints.md provides progressive help. Preserve input artifact versions, configuration, evaluator version, and seed with future scores. Review risk: Unaligned rows cause false skew. Equal values do not prove equal units, frames, transform identities, or correctness; validation of that metadata is outside this function.

## Editorial status

- [x] Paper card and manifest checked against the primary source.
- [x] Original contract, two examples, theory, visual, and text alternative drafted.
- [x] Exact Python/dependency versions specified; image digest honestly pending.
- [x] Independent draft-contract, mathematics, and pedagogy cross-review approved; implementation/evaluator review remains pending.
- [ ] Reference, public tests, and hidden tests implemented and isolated.
- [ ] Runtime image, measured limits, fixture hashes, and rendered accessibility approved.
- [ ] Publication authorized; this remains planned content.
