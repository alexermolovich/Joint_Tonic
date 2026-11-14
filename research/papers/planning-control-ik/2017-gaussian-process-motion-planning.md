---
schema_version: 1
paper_id: 2017-gaussian-process-motion-planning
title: Continuous-Time Gaussian Process Motion Planning via Probabilistic Inference
authors:
  - 'Mukadam, Mustafa'
  - 'Dong, Jing'
  - 'Yan, Xinyan'
  - 'Dellaert, Frank'
  - 'Boots, Byron'
year: 2017
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1707.07383'
pdf_url: 'https://arxiv.org/pdf/1707.07383'
local_pdf: ./2017-gaussian-process-motion-planning.pdf
sha256: 4aaa5b381fe91ec41b1ab8ce03c0a3edcae543b9a864746f31c8a9b7fc522385
bytes: 6541602
pages: 24
topics:
  - planning-control-ik
  - gaussian-process-motion-planning
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
      title: Build a trajectory prior
      detail: Represent smooth state evolution with a sparse Gaussian process.
      column: 0
      row: 0
      section: Build a trajectory prior
      problem_slugs:
        - gp-constant-velocity-factor
      planned_problems: []
    - id: stage-2
      title: Add obstacle factors
      detail: Penalize insufficient clearance along the robot body.
      column: 1
      row: 0
      section: Add obstacle factors
      problem_slugs:
        - assemble-motion-residuals
      planned_problems: []
    - id: stage-3
      title: Interpolate and optimize
      detail: Check intermediate states without introducing every one as a variable.
      column: 2
      row: 0
      section: Interpolate and optimize
      problem_slugs:
        - gp-support-interpolation
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: trajectory prior
    - from: stage-2
      to: stage-3
      label: sparse factor graph
---

## Core paper explanation

Gaussian-process motion planning treats a smooth continuous-time trajectory as a probabilistic prior and obstacles as likelihood factors. Sparse Markov structure makes trajectory optimization and interpolation efficient.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Build a trajectory prior

For stacked support states $\theta$, the prior is
$$p(\theta)\propto\exp[-\tfrac12(\theta-\mu)^\top K^{-1}(\theta-\mu)].$$
States may include configuration and velocity. A linear time-varying stochastic differential equation induces the sparse precision structure; an arbitrary dense GP kernel does not provide the same computational property.


**Component practice**

- [Build a Gaussian-Process Smoothness Factor](/problems/gp-constant-velocity-factor) — runnable bounded component; see its documented scope.

### Add obstacle factors

With signed distance $d(q)$ positive in free space, a teaching hinge residual is $h(q)=\max(0,\epsilon-d(q))$. The MAP objective becomes
$$E=\tfrac12\|\theta-\mu\|_{K^{-1}}^2+\tfrac12\|h(\theta)\|_{\Sigma^{-1}}^2.$$
Robot geometry and workspace distance fields determine the obstacle residuals.


**Component practice**

- [Assemble Obstacle and Prior Residuals](/problems/assemble-motion-residuals) — runnable bounded component; see its documented scope.

### Interpolate and optimize

GP interpolation estimates intermediate states from neighboring support states. Nonlinear least squares updates the support trajectory while evaluating obstacle factors at interpolated times. Finite interpolation checks do not by themselves prove continuous collision freedom.


**Component practice**

- [Interpolate a Trajectory Between Support States](/problems/gp-support-interpolation) — runnable bounded component; see its documented scope.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Runnable components and remaining ideas:**

- [Build a Gaussian-Process Smoothness Factor](/problems/gp-constant-velocity-factor) — runnable bounded component; see its documented scope.
- [Assemble Obstacle and Prior Residuals](/problems/assemble-motion-residuals) — runnable bounded component; see its documented scope.
- [Interpolate a Trajectory Between Support States](/problems/gp-support-interpolation) — runnable bounded component; see its documented scope.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Smoothness priors make optimization efficient and physically interpretable. A local optimizer can remain in a poor homotopy class or miss thin obstacles; initialization and independent collision validation remain necessary.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1707.07383) · [Open-access manuscript](https://arxiv.org/pdf/1707.07383)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
