---
schema_version: 1
paper_id: 2018-rmpflow
title: 'RMPflow: A Computational Graph for Automatic Motion Policy Generation'
authors:
  - 'Cheng, Ching-An'
  - 'Mukadam, Mustafa'
  - 'Issac, Jan'
  - 'Birchfield, Stan'
  - 'Fox, Dieter'
  - 'Boots, Byron'
  - 'Ratliff, Nathan'
year: 2018
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1811.07049'
pdf_url: 'https://arxiv.org/pdf/1811.07049'
local_pdf: ./2018-rmpflow.pdf
sha256: 069d06920ffdffd1e9ec3d4b562a1c016f81a9f9f803c59d271d25a6251f550c
bytes: 3396334
pages: 45
topics:
  - planning-control-ik
  - rmpflow
modalities:
  - joint-state
  - poses
  - obstacles
  - trajectories
track_role: supporting
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Follow the data through the mechanism. Training objectives and inference
    behavior are distinguished in the linked explanations.
  nodes:
    - id: stage-1
      title: Push task states forward
      detail: Map configuration and velocity into each task space.
      column: 0
      row: 0
      section: Push task states forward
      problem_slugs:
        - push-task-state
      planned_problems: []
    - id: stage-2
      title: Pull policies back
      detail: Combine natural-form forces and metrics in joint space.
      column: 1
      row: 0
      section: Pull policies back
      problem_slugs:
        - pullback-motion-metric
      planned_problems: []
    - id: stage-3
      title: Resolve the acceleration
      detail: Recover a joint acceleration from the combined natural form.
      column: 2
      row: 0
      section: Resolve the acceleration
      problem_slugs:
        - combine-motion-policies
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: task policies
    - from: stage-2
      to: stage-3
      label: root force and metric
---

## Core paper explanation

RMPflow composes local acceleration policies through a tree of task maps. Each policy carries a metric describing its directional importance, allowing goal attraction, obstacle avoidance, and other behaviors to combine consistently through robot kinematics.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Push task states forward

For task map $x=\psi(q)$ and Jacobian $J=\partial\psi/\partial q$,
$$\dot x=J\dot q,\qquad \ddot x=J\ddot q+\dot J\dot q.$$
$q$ contains joint coordinates; task coordinates may be positions, distances, or other quantities. Their units determine metric interpretation.


**Component practice**

- [Push Robot State into a Task Space](/problems/push-task-state) — runnable bounded component; see its documented scope.

### Pull policies back

For leaf natural forms $(f_i,M_i)$, the pullback is
$$M=\sum_iJ_i^\top M_iJ_i,\qquad f=\sum_iJ_i^\top(f_i-M_i\dot J_i\dot q).$$
The curvature term matters when task maps vary with configuration. Leaf forces themselves must include the geometric terms required by their chosen metric/policy construction.


**Component practice**

- [Pull Back a Local Motion Metric](/problems/pullback-motion-metric) — runnable bounded component; see its documented scope.

### Resolve the acceleration

The resolved policy is $\ddot q=M^\dagger f$, with pseudoinverse when necessary. Regularization and rank handling change behavior in weakly weighted directions. RMPflow is reactive policy composition; it is not a global obstacle-route planner.


**Component practice**

- [Combine Competing Task-Space Accelerations](/problems/combine-motion-policies) — runnable bounded component; see its documented scope.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Runnable components and remaining ideas:**

- [Push Robot State into a Task Space](/problems/push-task-state) — runnable bounded component; see its documented scope.
- [Pull Back a Local Motion Metric](/problems/pullback-motion-metric) — runnable bounded component; see its documented scope.
- [Combine Competing Task-Space Accelerations](/problems/combine-motion-policies) — runnable bounded component; see its documented scope.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Task-space behaviors can be reused across kinematic chains. Local minima, conflicting objectives, and incorrect Jacobian derivatives can still cause undesirable motion; the composition rules do not guarantee success for arbitrary leaf policies.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1811.07049) · [Open-access manuscript](https://arxiv.org/pdf/1811.07049)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
