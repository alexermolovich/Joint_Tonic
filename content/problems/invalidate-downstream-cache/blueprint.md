---
schema_version: 1
problem_id: invalidate-downstream-cache
content_version: 1.0.0
status: implemented
title: Invalidate Cached Artifacts After an Upstream Change
summary: >-
  Identify cached artifacts requiring recomputation after upstream versions
  change.
type: function
difficulty: medium
estimated_minutes: 30
domains:
  - robotics-mlops
topics:
  - artifact-lineage
  - cache-invalidation
paper_ids:
  - 2017-tfx-production-ml-platform
paper_sections:
  - 'Section 2.2: Platform Design and Anatomy; Figure 1'
track_ids: []
prerequisite_problem_ids:
  - dependency-graph-blast-radius
  - training-pipeline-topological-order
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
entrypoint: solution.invalidated_artifacts
physical_contract:
  frames: []
  units:
    ids: dimensionless
  axes: not-applicable
  timestamp_assumptions: >-
    One immutable dependency snapshot; changed means an external version
    comparison already found a change.
  batching: One artifact graph and cache snapshot per call.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - uncached intermediate
    - changed cached root
    - empty change set
  hidden_case_families:
    - duplicate parent entries
    - overlapping change sets
    - unknown cached IDs
    - cyclic disconnected component
    - unrelated cache branch
  performance_class: none; no timing leaderboard
  evaluator_sha256: a342a7d451527fa19b357f89eb618751ed29bc7cb6e4880c750d505a8ca237d6
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: 'sha256:a342a7d451527fa19b357f89eb618751ed29bc7cb6e4880c750d505a8ca237d6'
  generated_fixture_hash: a342a7d451527fa19b357f89eb618751ed29bc7cb6e4880c750d505a8ca237d6
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
# Invalidate Cached Artifacts After an Upstream Change

## Learning objective

Identify cached artifacts requiring recomputation after upstream versions change.

## Paper connection and scope

TFX motivates explicit pipeline artifacts and dependencies. This conservative invalidation policy is original; it does not reproduce a TFX cache-key format. Source location: Section 2.2: Platform Design and Anatomy; Figure 1. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).

## Contract and worked examples

Return cached IDs in the changed-or-downstream closure of a validated DAG. Dependencies map a consumer to its parents. Propagate through uncached artifacts, but return cached artifacts only. problem.md is the normative input/error/output specification; examples.md expands its two public examples. Inputs must not be mutated. The reference and public/hidden cases passed the local isolated worker.

## Starter code

starter.py supplies the signature; reference.py implements the reviewed contract. No networking, filesystem access, or simulator control belongs in learner code.

## Reference solution

Validate the full DAG, reverse consumer-to-parent lists into parent-to-consumer adjacency, traverse changed roots, intersect with the cached set, and sort. O(V + E + V log V) time and O(V + E) memory. Do not mutate or delete artifacts.

## Evaluator plan

Public families: uncached intermediate; changed cached root; empty change set. Hidden families: duplicate parent entries; overlapping change sets; unknown cached IDs; cyclic disconnected component; unrelated cache branch. Compare order, shape, and dtype exactly; apply the stated numerical tolerances where relevant. Validate errors by exception type rather than message. Check input immutability. Seed generated fixtures with 20261113; no wall-clock timing or network enters correctness grading. Report platform setup failures separately from learner failures. The reference passed eight public/hidden cases in submit mode and three public cases in run mode; the starter was rejected. cases.py pins evaluator and synthetic fixture source. The OCI image digest remains pending; execution used the stated local baseline.

## Visualization plan

Original changed-data-to-cached-report graph and inclusion table; static text alternative. This is a Markdown diagram specification, not a claim that today's renderer supports Mermaid. Keep the static text/table fallback usable before publication.

## Theory, hints, and reproducibility

Read theory.md for intuition, defined math, a worked example, robot failure modes, and conceptual questions. hints.md provides progressive help. Preserve input artifact versions, configuration, evaluator version, and seed with future scores. Review risk: Stopping at an uncached intermediate misses stale descendants. Inputs are declarations of change, not hashes; this exercise cannot detect undeclared changes or decide numerical equivalence.

## Editorial status

- [x] Paper card and manifest checked against the primary source.
- [x] Original contract, two examples, theory, visual, and text alternative drafted.
- [x] Exact Python/dependency versions specified; image digest honestly pending.
- [x] Independent draft-contract, mathematics, and pedagogy cross-review approved; implementation/evaluator review remains pending.
- [x] Reference, public tests, and hidden tests passed the actual local bubblewrap worker.
- [ ] Runtime image, measured limits, fixture hashes, and rendered accessibility approved.
- [x] Local runnable integration authorized; production publication remains separate.
