---
schema_version: 1
problem_id: training-pipeline-topological-order
content_version: 1.0.0
status: implemented
title: Topologically Schedule a Training Pipeline DAG
summary: >-
  Produce a deterministic valid execution order for an artifact-dependent
  training pipeline.
type: function
difficulty: medium
estimated_minutes: 30
domains:
  - robotics-mlops
topics:
  - pipeline-orchestration
  - dependency-order
paper_ids:
  - 2017-tfx-production-ml-platform
paper_sections:
  - 'Section 2.2 and Figure 1: platform components and orchestration context'
track_ids: []
prerequisite_problem_ids:
  - dependency-graph-blast-radius
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
entrypoint: solution.schedule_pipeline
physical_contract:
  frames: []
  units:
    ids: dimensionless
  axes: not-applicable
  timestamp_assumptions: 'Logical precedence only; no durations, timestamps, resources, or execution.'
  batching: One complete pipeline graph per call.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - newly ready lexical priority
    - two-input merge
    - empty graph
  hidden_case_families:
    - duplicate edges
    - disconnected stages
    - disconnected cycle
    - self-loop
    - undeclared endpoints
    - deep pipeline
  performance_class: none; no timing leaderboard
  evaluator_sha256: a6558a5fc8901e8cfde51ecee3ca05a1871de21c0de15d92363a2111eb455dd8
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: 'sha256:a6558a5fc8901e8cfde51ecee3ca05a1871de21c0de15d92363a2111eb455dd8'
  generated_fixture_hash: a6558a5fc8901e8cfde51ecee3ca05a1871de21c0de15d92363a2111eb455dd8
provenance:
  authoring_notes: >-
    Original instructional contract, examples, and diagrams; no copied paper
    code or figures.
  primary_urls:
    - >-
      https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/
  implementation_urls: []
  paper_card: research/papers/mlops-sim2real/2017-tfx-production-ml-platform.md
  manifest: research/manifests/mlops-sim2real.md
owners:
  - code_issue_scout
reviewers:
  - ui_issue_scout
derived_draft_version: 0.1.0
---
# Topologically Schedule a Training Pipeline DAG

## Learning objective

Produce a deterministic valid execution order for an artifact-dependent training pipeline.

## Paper connection and scope

The pipeline context comes from TFX. Lexicographic topological scheduling is this exercise's original operational component, not a claim about the paper's scheduler. Source location: Section 2.2 and Figure 1: platform components and orchestration context. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).

## Contract and worked examples

Return a lexicographically minimal topological order of all declared stages. Reject any cycle, including disconnected cycles. Duplicate edges count once. problem.md is the normative input/error/output specification; examples.md expands its two public examples. Inputs must not be mutated. The reference and public/hidden cases passed the local isolated worker.

## Starter code

starter.py provides the signature; reference.py implements the reviewed contract. No networking, filesystem access, or simulator control belongs in learner code.

## Reference solution

Deduplicate edges, track remaining indegrees, and choose the smallest currently ready ID with a min-heap. Decrement consumers after each stage. If fewer than V nodes are emitted, raise ValueError. O(V + E + V log V) time and O(V + E) memory.

## Evaluator plan

Public families: newly ready lexical priority; two-input merge; empty graph. Hidden families: duplicate edges; disconnected stages; disconnected cycle; self-loop; undeclared endpoints; deep pipeline. Compare order, shape, and dtype exactly; apply the stated numerical tolerances where relevant. Validate errors by exception type rather than message. Check input immutability. Seed generated fixtures with 20261113; no wall-clock timing or network enters correctness grading. Report platform setup failures separately from learner failures. cases.py pins the evaluator and synthetic fixtures. The reference passed all 8 cases in submit mode and three public cases in run mode; the starter fails public cases as expected. The OCI image digest remains pending; execution used the stated local baseline.

## Visualization plan

Original ready-set/merge graph with a step table in theory.md; text alternative and no motion. This is a Markdown diagram specification, not a claim that today's renderer supports Mermaid. Keep the static text/table fallback usable before publication.

## Theory, hints, and reproducibility

Read theory.md for intuition, defined math, a worked example, robot failure modes, and conceptual questions. hints.md provides progressive help. Preserve input artifact versions, configuration, evaluator version, and seed with future scores. Review risk: Sorting a complete list or only sorting initial stages is insufficient. A newly ready stage can precede an already waiting one. Reject partial schedules when any cycle remains.

## Editorial status

- [x] Paper card and manifest checked against the primary source.
- [x] Original contract, two examples, theory, visual, and text alternative drafted.
- [x] Exact Python/dependency versions specified; image digest honestly pending.
- [x] Independent draft-contract, mathematics, and pedagogy cross-review approved; implementation/evaluator review remains pending.
- [x] Reference, public tests, and hidden tests passed the real local bubblewrap worker.
- [ ] Runtime image, measured limits, fixture hashes, and rendered accessibility approved.
- [x] Local runnable integration authorized. Hosted/production publication remains separate.
