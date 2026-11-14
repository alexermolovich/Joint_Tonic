---
schema_version: 1
problem_id: detect-pipeline-feedback-loops
content_version: 0.1.0
status: reviewed
title: Detect Feedback Loops in an ML Pipeline
summary: >-
  Group declared pipeline components that participate in the same directed
  feedback cycle.
type: function
difficulty: medium
estimated_minutes: 30
domains:
  - robotics-mlops
topics:
  - dependency-management
  - feedback-cycles
paper_ids:
  - 2015-hidden-technical-debt
paper_sections:
  - 'Section4: Feedback Loops'
track_ids: []
prerequisite_problem_ids:
  - dependency-graph-blast-radius
runtime:
  language: python
  python: 3.12.3
  runtime_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
  image_digest: null
  image_status: pending OCI build; baseline worker exists
  dependencies: {}
  platform: linux-x86_64-cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  budget_status: actual shared worker limits; this draft has not run
entrypoint: solution.feedback_groups
physical_contract:
  frames: []
  units:
    ids: dimensionless component labels
  axes: Directed edge from producer/influencer to consumer.
  timestamp_assumptions: One dependency snapshot; cycles may span future collection/training runs.
  batching: One directed graph per call.
grading:
  mode: exact
  seed: 20261113
  rtol: 0
  atol: 0
  public_case_families:
    - one feedback group
    - self-loop and two-node cycle
    - empty graph
  hidden_case_families:
    - acyclic descendants
    - overlapping cycles
    - duplicate edges
    - long iterative traversal
    - invalid IDs and bounds
  performance_class: none; no timing leaderboard
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: mlops-batch2-draft-0.1.0
  evaluator_sha256: null
provenance:
  authoring_notes: >-
    The paper motivates inspecting direct and indirect feedback. Strongly
    connected components are an original finite-graph teaching tool; declared
    graph cycles do not prove a harmful statistical feedback effect, and absent
    edges can hide real loops.
  primary_urls:
    - >-
      https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html
  implementation_urls: []
  paper_card: research/papers/mlops-sim2real/2015-hidden-technical-debt.md
  manifest: research/manifests/mlops-sim2real.md
owners:
  - code_issue_scout
reviewers:
  - perception_implementation
---

# Detect Feedback Loops in an ML Pipeline

## Learning objective

Group declared pipeline components that participate in the same directed feedback cycle.

## Source and scope

The paper motivates inspecting direct and indirect feedback. Strongly connected components are an original finite-graph teaching tool; declared graph cycles do not prove a harmful statistical feedback effect, and absent edges can hide real loops. Source location: Section4: Feedback Loops. [Primary source](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate the snapshot; run iterative Kosaraju traversal, retaining cyclic components. O(V+E+V log V) time including deterministic sorting, O(V+E) storage. No recursion dependency.

## Evaluator plan

Public cases: one feedback group; self-loop and two-node cycle; empty graph. Hidden cases: acyclic descendants; overlapping cycles; duplicate edges; long iterative traversal; invalid IDs and bounds. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
