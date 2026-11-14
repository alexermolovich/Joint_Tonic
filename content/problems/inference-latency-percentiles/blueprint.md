---
schema_version: 1
problem_id: inference-latency-percentiles
content_version: 1.0.0
status: implemented
title: 'Compute p50, p90, and p99 Inference Latency'
summary: >-
  Summarize end-to-end request latency with explicitly defined nearest-rank p50,
  p90, and p99 values.
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - robotics-mlops
topics:
  - latency
  - benchmarking
  - measurement
paper_ids:
  - 2019-mlperf-inference
paper_sections:
  - >-
    Section IV inference scenarios and Table II; percentile calculation is a
    declared teaching convention
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; tested using the local bubblewrap baseline
  dependencies:
    numpy: 2.2.4
    torch: 2.6.0+cpu
  platform: linux-x86_64-cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  budget_status: actual shared worker caps; per-process address-space limit
  solution_dependencies: []
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
entrypoint: solution.latency_percentiles
physical_contract:
  frames: []
  units:
    timestamps: nanoseconds
    outputs: milliseconds
  axes: not-applicable
  timestamp_assumptions: >-
    Paired request arrival/completion on one monotonic clock; integer
    nanoseconds with a shared arbitrary origin.
  batching: Two lists of N paired requests; no batch-size weighting or warmup filtering.
grading:
  mode: numerical
  seed: 20261113
  rtol: 0
  atol: 1.e-9
  public_case_families:
    - long tail
    - even sample count
    - empty trace
  hidden_case_families:
    - single zero-duration query
    - out-of-order completions
    - large clock origins with small differences
    - invalid clock direction
    - bool/noninteger rejection
    - duplicate durations
  performance_class: none; no timing leaderboard
  evaluator_sha256: 6efe41efa226b1e5406194da99f8feb3bb26e0a68b4aa36356a12a90ea833b89
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: 'sha256:6efe41efa226b1e5406194da99f8feb3bb26e0a68b4aa36356a12a90ea833b89'
  generated_fixture_hash: 6efe41efa226b1e5406194da99f8feb3bb26e0a68b4aa36356a12a90ea833b89
provenance:
  authoring_notes: >-
    Original instructional contract, examples, and diagrams; no copied paper
    code or figures.
  primary_urls:
    - 'https://arxiv.org/abs/1911.02549'
  implementation_urls: []
  paper_card: research/papers/mlops-sim2real/2019-mlperf-inference.md
  manifest: research/manifests/mlops-sim2real.md
owners:
  - code_issue_scout
reviewers:
  - ui_issue_scout
derived_draft_version: 0.1.0
---
# Compute p50, p90, and p99 Inference Latency

## Learning objective

Summarize end-to-end request latency with explicitly defined nearest-rank p50, p90, and p99 values.

## Paper connection and scope

MLPerf motivates scenario-aware latency measurement. These three statistics and the estimator below are educational diagnostics, not a current MLPerf compliance checker. Source location: Section IV inference scenarios and Table II; percentile calculation is a declared teaching convention. [Primary source](https://arxiv.org/abs/1911.02549).

## Contract and worked examples

Subtract paired integer timestamps, sort durations, select one-based ranks ceil(p*N), and convert nanoseconds to milliseconds. Empty observations produce three None values. problem.md is the normative input/error/output specification; examples.md expands its two public examples. Inputs must not be mutated. The reference and public/hidden cases passed the local isolated worker.

## Starter code

starter.py supplies the signature; reference.py implements the reviewed contract. No networking, filesystem access, or simulator control belongs in learner code.

## Reference solution

Validate before computing. Subtract Python integer timestamps before any float conversion; sort durations once, select integer ranks (percent*N+99)//100, then divide by 1,000,000. O(N log N) time and O(N) memory.

## Evaluator plan

Public families: long tail; even sample count; empty trace. Hidden families: single zero-duration query; out-of-order completions; large clock origins with small differences; invalid clock direction; bool/noninteger rejection; duplicate durations. Compare order, shape, and dtype exactly; apply the stated numerical tolerances where relevant. Validate errors by exception type rather than message. Check input immutability. Seed generated fixtures with 20261113; no wall-clock timing or network enters correctness grading. Report platform setup failures separately from learner failures. The reference passed eight public/hidden cases in submit mode and three public cases in run mode; the starter was rejected. cases.py pins evaluator and synthetic fixture source. The OCI image digest remains pending; execution used the stated local baseline.

## Visualization plan

Original arrival-to-completion pipeline and sorted-duration/rank table; static text alternative. This is a Markdown diagram specification, not a claim that today's renderer supports Mermaid. Keep the static text/table fallback usable before publication.

## Theory, hints, and reproducibility

Read theory.md for intuition, defined math, a worked example, robot failure modes, and conceptual questions. hints.md provides progressive help. Preserve input artifact versions, configuration, evaluator version, and seed with future scores. Review risk: Percentiles are estimator-dependent; p50 is not the average of the central pair here. Mixing clocks or timing only launch submission undercounts actual robot latency.

## Editorial status

- [x] Paper card and manifest checked against the primary source.
- [x] Original contract, two examples, theory, visual, and text alternative drafted.
- [x] Exact Python/dependency versions specified; image digest honestly pending.
- [x] Independent draft-contract, mathematics, and pedagogy cross-review approved; implementation/evaluator review remains pending.
- [x] Reference, public tests, and hidden tests passed the actual local bubblewrap worker.
- [ ] Runtime image, measured limits, fixture hashes, and rendered accessibility approved.
- [x] Local runnable integration authorized; production publication remains separate.
