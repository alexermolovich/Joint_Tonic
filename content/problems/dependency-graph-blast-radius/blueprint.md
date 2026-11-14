---
schema_version: 1
problem_id: dependency-graph-blast-radius
content_version: 1.0.0
status: implemented
title: Compute Dependency-Graph Blast Radius
summary: Identify declared downstream consumers affected by a component change.
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - robotics-mlops
topics:
  - dependency-management
  - change-impact
paper_ids:
  - 2015-hidden-technical-debt
paper_sections:
  - 'Section 2: Undeclared Consumers; Section 3: Data Dependencies'
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
entrypoint: solution.blast_radius
physical_contract:
  frames: []
  units:
    ids: dimensionless
  axes: not-applicable
  timestamp_assumptions: One immutable dependency snapshot; no event time.
  batching: One graph and one changed set per call.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - branched pipeline
    - feedback cycle
    - empty changed set
  hidden_case_families:
    - multiple roots
    - duplicate edges/roots
    - self-loop
    - unknown IDs
    - long chain
  performance_class: none; no timing leaderboard
  evaluator_sha256: b2523f7a6d25c7f11a7900bd9f7b7e60d76808e6d26e3a92a7858744062d2e51
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: 'sha256:b2523f7a6d25c7f11a7900bd9f7b7e60d76808e6d26e3a92a7858744062d2e51'
  generated_fixture_hash: b2523f7a6d25c7f11a7900bd9f7b7e60d76808e6d26e3a92a7858744062d2e51
provenance:
  authoring_notes: >-
    Original instructional contract, examples, and diagrams; no copied paper
    code or figures.
  primary_urls:
    - >-
      https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html
  implementation_urls: []
  paper_card: research/papers/mlops-sim2real/2015-hidden-technical-debt.md
  manifest: research/manifests/mlops-sim2real.md
owners:
  - code_issue_scout
reviewers:
  - ui_issue_scout
derived_draft_version: 0.1.0
---
# Compute Dependency-Graph Blast Radius

## Learning objective

Identify declared downstream consumers affected by a component change.

## Paper connection and scope

The source motivates inspecting system dependencies. Reachability and ordering here are original teaching rules, not a paper-defined metric. Source location: Section 2: Undeclared Consumers; Section 3: Data Dependencies. [Primary source](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html).

## Contract and worked examples

Return sorted unique downstream nodes, excluding every changed root. Cycles are allowed; undeclared IDs are errors. problem.md is the normative input/error/output specification; examples.md expands its two public examples. Inputs must not be mutated. The reference and public/hidden cases passed the local isolated worker.

## Starter code

starter.py provides the signature; reference.py implements the reviewed contract. No networking, filesystem access, or simulator control belongs in learner code.

## Reference solution

Build producer-to-consumer adjacency; traverse from changed roots with a visited set, subtract roots, and sort. O(V + E + V log V) worst-case time, O(V + E) memory. Use iterative traversal to avoid recursion depth.

## Evaluator plan

Public families: branched pipeline; feedback cycle; empty changed set. Hidden families: multiple roots; duplicate edges/roots; self-loop; unknown IDs; long chain. Compare order, shape, and dtype exactly; apply the stated numerical tolerances where relevant. Validate errors by exception type rather than message. Check input immutability. Seed generated fixtures with 20261113; no wall-clock timing or network enters correctness grading. Report platform setup failures separately from learner failures. cases.py pins the evaluator and synthetic fixtures. The reference passed all 9 cases in submit mode and three public cases in run mode; the starter fails public cases as expected. The OCI image digest remains pending; execution used the stated local baseline.

## Visualization plan

Original dependency graph and expansion table in theory.md; static, with text alternative. This is a Markdown diagram specification, not a claim that today's renderer supports Mermaid. Keep the static text/table fallback usable before publication.

## Theory, hints, and reproducibility

Read theory.md for intuition, defined math, a worked example, robot failure modes, and conceptual questions. hints.md provides progressive help. Preserve input artifact versions, configuration, evaluator version, and seed with future scores. Review risk: Missing graph edges hide real consumers. Cycles must terminate, and roots remain excluded when reached again.

## Editorial status

- [x] Paper card and manifest checked against the primary source.
- [x] Original contract, two examples, theory, visual, and text alternative drafted.
- [x] Exact Python/dependency versions specified; image digest honestly pending.
- [x] Independent draft-contract, mathematics, and pedagogy cross-review approved; implementation/evaluator review remains pending.
- [x] Reference, public tests, and hidden tests passed the real local bubblewrap worker.
- [ ] Runtime image, measured limits, fixture hashes, and rendered accessibility approved.
- [x] Local runnable integration authorized. Hosted/production publication remains separate.
