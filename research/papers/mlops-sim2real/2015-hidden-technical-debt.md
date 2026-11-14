---
schema_version: 1
paper_id: 2015-hidden-technical-debt
title: Hidden Technical Debt in Machine Learning Systems
authors:
  - D. Sculley
  - Gary Holt
  - Daniel Golovin
  - Eugene Davydov
  - Todd Phillips
  - Dietmar Ebner
  - Vinay Chaudhary
  - Michael Young
  - Jean-Francois Crespo
  - Dan Dennison
year: 2015
venue_or_status: NeurIPS 2015
primary_url: >-
  https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html
pdf_url: >-
  https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf
local_pdf: ./2015-hidden-technical-debt.pdf
sha256: 1a67da09a8bd5ba9a3577176e30aa2fbd88534e6baf0bc31522b4999f643d2a1
bytes: 165614
pages: 9
topics:
  - mlops
  - technical-debt
  - dependency-management
  - monitoring
  - production-ml
modalities:
  - system-graphs
  - metadata
  - operational-metrics
track_role: foundation
open_access_status: open-access-proceedings
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Map dependencies, trace the impact of a proposed change, and attach evidence
    to release/monitoring decisions.
  nodes:
    - id: stage-1
      title: Map system dependencies
      detail: >-
        Record data sources, transforms, models, and downstream consumers as a
        directed graph.
      column: 0
      row: 0
      section: Map system dependencies
      problem_slugs:
        - dependency-graph-blast-radius
      planned_problems: []
    - id: stage-2
      title: Inspect coupling and feedback
      detail: Find changes that can alter both predictions and future training inputs.
      column: 1
      row: 0
      section: Inspect coupling and feedback
      problem_slugs:
        - detect-pipeline-feedback-loops
      planned_problems: []
    - id: stage-3
      title: Control and observe changes
      detail: 'Make ownership, validation, rollback, and consumer contracts explicit.'
      column: 2
      row: 0
      section: Control and observe changes
      problem_slugs:
        - slice-infrastructure-release-gate
        - physical-ai-incident-triage
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: dependency graph
    - from: stage-2
      to: stage-3
      label: impact analysis
---

## Core paper explanation

Hidden Technical Debt in Machine Learning Systems explains why a model’s surrounding data and software dependencies can dominate long-term maintenance cost. Changing one feature or dataset can affect many downstream consumers; feedback loops can change the data that future training receives. The paper is a systems analysis, not a new learning algorithm. The equations here are explicit teaching models for reasoning about its dependency risks.

## Execution flow

Map dependencies, trace the impact of a proposed change, and attach evidence to release/monitoring decisions.

### Map system dependencies

Let $G=(V,E)$ be a dependency graph and $A$ its adjacency matrix, with $A_{ij}=1$ when component $j$ consumes component $i$. The transitive reachability set of changed component $i$ is

$$
R(i)=\{j:\exists k\ge1,\ (A^k)_{ij}>0\}.
$$

This formalizes change propagation; it is not a metric defined by the source paper. Undeclared consumers create missing edges, so a perfectly computed reachability set can still understate real impact.


**Component practice**

- Runnable component: [Compute Dependency-Graph Blast Radius](/problems/dependency-graph-blast-radius). Implements the bounded learning contract linked here, not the complete paper.

### Inspect coupling and feedback

A feedback loop exists when a component can reach itself through a nonempty directed path. A simple operational model is

$$
D_{t+1}=F(D_t,\pi_t,\mathrm{environment}),\qquad\pi_{t+1}=\operatorname{Train}(D_{t+1}).
$$

The deployed policy $\pi_t$ influences future data $D_{t+1}$, so training data is not necessarily independent of earlier model decisions. Monitor this pathway rather than assuming a static dataset distribution.


**Component practice**

- Runnable component: [Detect Feedback Loops in an ML Pipeline](/problems/detect-pipeline-feedback-loops). Uses the bounded contract; no full paper reproduction is claimed.

### Control and observe changes

A transparent change gate can require every affected critical component to have fresh evidence:

$$
\mathrm{ready}=\bigwedge_{j\in R(i)\cap V_{\mathrm{critical}}}\mathrm{evidenceValid}(j).
$$

This is a teaching policy, not the paper’s prescribed numeric score. Unknown evidence should remain unknown rather than being converted to a passing value. Record the version of inputs, transforms, models, and evaluators together.


**Component practice**

- Supporting prerequisite: [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate). Uses the bounded contract; no full paper reproduction is claimed.
- Supporting prerequisite: [Triage a Physical-AI Deployment Incident](/problems/physical-ai-incident-triage). Uses the bounded contract; no full paper reproduction is claimed.

## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Runnable component:** [Compute Dependency-Graph Blast Radius](/problems/dependency-graph-blast-radius).
- **Runnable component:** [Detect Feedback Loops in an ML Pipeline](/problems/detect-pipeline-feedback-loops).
- **Supporting prerequisite:** [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate).
- **Supporting prerequisite:** [Triage a Physical-AI Deployment Incident](/problems/physical-ai-incident-triage).

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

A robot policy changes what the robot observes, which objects it interacts with, and which failures enter the next dataset. Untracked data and calibration dependencies can make a small update unsafe or hard to diagnose. Dependency visibility is useful even when the neural network itself is unchanged.

## Sources and scope

[Primary paper](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) · [Open-access manuscript](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
