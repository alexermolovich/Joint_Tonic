---
schema_version: 1
paper_id: "2018-dynamics-randomization"
title: "Sim-to-Real Transfer of Robotic Control with Dynamics Randomization"
authors:
  - "Xue Bin Peng"
  - "Marcin Andrychowicz"
  - "Wojciech Zaremba"
  - "Pieter Abbeel"
year: 2018
venue_or_status: "IEEE ICRA 2018"
primary_url: "https://arxiv.org/abs/1710.06537"
pdf_url: "https://arxiv.org/pdf/1710.06537"
local_pdf: "./2018-dynamics-randomization.pdf"
sha256: "a15cb24630a11218865027024ae2353f80f46d40371b42dccb2b24e9d00d62d8"
bytes: 2845918
pages: 8
topics:
  - "sim-to-real"
  - "dynamics-randomization"
  - "reinforcement-learning"
  - "robust-control"
  - "calibration"
modalities:
  - "robot-state"
  - "actions"
  - "rewards"
  - "dynamics-parameters"
  - "trajectories"
track_role: "core"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Sample physical parameters, run policy rollouts under those dynamics, and evaluate transfer across parameter and hardware conditions.","nodes":[{"id":"stage-1","title":"Sample a physical model","detail":"Choose valid simulator parameters with declared units and reset semantics.","column":0,"row":0,"section":"Sample a physical model","problem_slugs":["sample-dynamics-distributions"],"planned_problems":["Version a Simulation Scenario Distribution"]},{"id":"stage-2","title":"Optimize expected return","detail":"Train a policy across the parameter distribution rather than one nominal environment.","column":1,"row":0,"section":"Optimize expected return","problem_slugs":[],"planned_problems":["Aggregate Mean and Worst-Case Policy Returns"]},{"id":"stage-3","title":"Evaluate parameter slices","detail":"Separate average success from weak regions of the physical parameter space.","column":2,"row":0,"section":"Evaluate parameter slices","problem_slugs":[],"planned_problems":["Quantify Calibration Sensitivity","Choose Randomization Bounds from Safety Constraints","Gate Sim-to-Real Release with Robustness Evidence"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"randomized dynamics"},{"from":"stage-2","to":"stage-3","label":"trained controller"}]}
---

## Core paper explanation

Dynamics randomization trains a policy across simulated physical models rather than one nominal model. Randomized masses, friction, damping, actuation, and other parameters expose the policy to uncertainty that can resemble the sim-to-real gap. The distribution and control interface determine what robustness is actually being trained; a robust policy under one parameter family can still fail outside it.

## Execution flow

Sample physical parameters, run policy rollouts under those dynamics, and evaluate transfer across parameter and hardware conditions.

### Sample a physical model

Let $\xi$ specify dynamics and let $P_\xi(s_{t+1}\mid s_t,a_t)$ be the corresponding transition model. Sample $\xi\sim p(\xi)$ at the declared reset boundary. Mass must remain positive, inertia physically valid, and latency expressed in the same time unit as the simulator.


**Component practice**

- Runnable component: [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions). Implements the bounded learning contract linked here, not the complete paper.
- Version a Simulation Scenario Distribution — unreviewed idea; contract and evaluator required.

### Optimize expected return

The objective can be expressed as

$$
J(\theta)=\mathbb E_{\xi\sim p,\,\tau\sim\pi_\theta,P_\xi}
\left[\sum_{t=0}^{T-1}\gamma^t r(s_t,a_t)\right].
$$

The policy may not directly observe $\xi$, so history can help infer its effects. Resampling every physics step is a different problem from keeping parameters fixed for an episode; the choice changes what the policy must learn.


**Component practice**

- Aggregate Mean and Worst-Case Policy Returns — unreviewed idea; contract and evaluator required.

### Evaluate parameter slices

For parameter bucket $b$, estimate $\hat J_b=N_b^{-1}\sum_nR_n$. Report $N_b$, uncertainty, and failure categories. A useful extension is a lower-tail return statistic, but it should be labeled separately from the paper’s own evaluation. Replay exact physics parameters and seeds when investigating failures.


**Component practice**

- Quantify Calibration Sensitivity — unreviewed idea; contract and evaluator required.
- Choose Randomization Bounds from Safety Constraints — unreviewed idea; contract and evaluator required.
- Gate Sim-to-Real Release with Robustness Evidence — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Runnable component:** [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions).

**Planned component problems:**

- Version a Simulation Scenario Distribution — unreviewed idea; contract and evaluator required.
- Aggregate Mean and Worst-Case Policy Returns — unreviewed idea; contract and evaluator required.
- Quantify Calibration Sensitivity — unreviewed idea; contract and evaluator required.
- Choose Randomization Bounds from Safety Constraints — unreviewed idea; contract and evaluator required.
- Gate Sim-to-Real Release with Robustness Evidence — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Randomization can make a policy less brittle to physical mismatch, but unmodeled backlash, contacts, wear, and sensor delay can remain. Ensure the randomized simulator itself is stable; otherwise the policy may learn around numerical artifacts instead of real uncertainty.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1710.06537) · [Open-access manuscript](https://arxiv.org/pdf/1710.06537)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
