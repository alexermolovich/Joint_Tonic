---
schema_version: 1
paper_id: 2010-rrt-star
title: Incremental Sampling-based Algorithms for Optimal Motion Planning
authors:
  - 'Karaman, Sertac'
  - 'Frazzoli, Emilio'
year: 2010
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1005.0416'
pdf_url: 'https://arxiv.org/pdf/1005.0416'
local_pdf: ./2010-rrt-star.pdf
sha256: 30310e5d83a6f9a76dcb81f310785456a72453dba5794cba1cd4005690818ac6
bytes: 9436806
pages: 20
topics:
  - planning-control-ik
  - rrt-star
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
      title: Sample and extend
      detail: Connect a new configuration toward a random sample.
      column: 0
      row: 0
      section: Sample and extend
      problem_slugs:
        - nearby-planning-tree-vertices
      planned_problems: []
    - id: stage-2
      title: Choose a low-cost parent
      detail: Compare collision-free connections within a shrinking neighborhood.
      column: 1
      row: 0
      section: Choose a low-cost parent
      problem_slugs:
        - minimum-cost-tree-parent
      planned_problems: []
    - id: stage-3
      title: Rewire and update costs
      detail: Replace more expensive routes through the new vertex.
      column: 2
      row: 0
      section: Rewire and update costs
      problem_slugs:
        - rewire-planning-tree
        - planning-budget-comparison
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: new configuration
    - from: stage-2
      to: stage-3
      label: selected parent
---

## Core paper explanation

RRT* improves a sampling-based tree by choosing lower-cost parents and rewiring nearby nodes. Under the paper’s assumptions, increasing samples drives solution cost toward the optimum; finite-time runs still need explicit feasibility and quality checks.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Sample and extend

Sample $q_{\mathrm{rand}}$ in configuration space, find a nearby tree vertex, and steer at most a prescribed distance. Collision checking must cover the connecting motion, not only its endpoints. Joint-space distances require explicit treatment of angular wraparound and mixed units.


**Component practice**

- [Find Nearby Planning Tree Vertices](/problems/nearby-planning-tree-vertices) — runnable bounded component; see its documented scope.

### Choose a low-cost parent

In $d$ dimensions, a typical radius is
$$r_n=\min\!\left(\gamma(\log n/n)^{1/d},\eta\right).$$
Choose $q_p=\arg\min_{q\in\mathcal N}[c(q)+c(q,q_{\mathrm{new}})]$ among feasible connections. $c(q)$ is root-to-node cost; $\gamma$ must satisfy the theorem's domain-dependent conditions for the asymptotic claim.


**Component practice**

- [Choose a Collision-Free Minimum-Cost Tree Parent](/problems/minimum-cost-tree-parent) — runnable bounded component; see its documented scope.

### Rewire and update costs

Reparent neighbor $q$ when $c(q_{\mathrm{new}})+c(q_{\mathrm{new}},q)<c(q)$ and the edge is valid. Propagate changed costs to descendants and prevent cycles. The original analysis concerns geometric planning assumptions; dynamic feasibility needs an appropriate steering model.


**Component practice**

- [Rewire a Tree Without Creating Cycles](/problems/rewire-planning-tree) — runnable bounded component; see its documented scope.
- [Compare Path Cost Across Sampling Budgets](/problems/planning-budget-comparison) — runnable bounded component; see its documented scope.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Runnable components and remaining ideas:**

- [Find Nearby Planning Tree Vertices](/problems/nearby-planning-tree-vertices) — runnable bounded component; see its documented scope.
- [Choose a Collision-Free Minimum-Cost Tree Parent](/problems/minimum-cost-tree-parent) — runnable bounded component; see its documented scope.
- [Rewire a Tree Without Creating Cycles](/problems/rewire-planning-tree) — runnable bounded component; see its documented scope.
- [Compare Path Cost Across Sampling Budgets](/problems/planning-budget-comparison) — runnable bounded component; see its documented scope.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Rewiring can improve paths without discarding prior search effort. Narrow passages, inaccurate collision geometry, and a mismatched steering model remain practical obstacles; asymptotic optimality is not a deadline guarantee.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1005.0416) · [Open-access manuscript](https://arxiv.org/pdf/1005.0416)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
