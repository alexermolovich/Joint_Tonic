---
schema_version: 1
paper_id: 2021-implicit-q-learning
title: Offline Reinforcement Learning with Implicit Q-Learning
authors:
  - 'Kostrikov, Ilya'
  - 'Nair, Ashvin'
  - 'Levine, Sergey'
year: 2021
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2110.06169'
pdf_url: 'https://arxiv.org/pdf/2110.06169'
local_pdf: ./2021-implicit-q-learning.pdf
sha256: b135fecfc6685b5ac88c5d41d2f78db8da03ce3e47c8e1152cb1f77a1ffa59ee
bytes: 476109
pages: 13
topics:
  - robot-learning-rl
  - implicit-q-learning
modalities:
  - robot-state
  - rgb
  - actions
  - rewards
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
      title: Fit an expectile value
      detail: Weight positive and negative residuals asymmetrically.
      column: 0
      row: 0
      section: Fit an expectile value
      problem_slugs:
        - iql-expectile-regression
      planned_problems: []
    - id: stage-2
      title: Back up the critic
      detail: Use the learned value without sampling an out-of-dataset maximizer.
      column: 1
      row: 0
      section: Back up the critic
      problem_slugs:
        - soft-value-bellman-target
        - iql-offline-dataset-split
      planned_problems: []
    - id: stage-3
      title: Extract an advantage-weighted policy
      detail: Prefer better logged actions while retaining supervised fitting.
      column: 2
      row: 0
      section: Extract an advantage-weighted policy
      problem_slugs:
        - iql-advantage-action-weights
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: expectile value
    - from: stage-2
      to: stage-3
      label: critic and value
---

## Core paper explanation

IQL learns from offline data without maximizing Q over unseen actions during critic fitting. It estimates an upper expectile value from dataset actions, then extracts a policy through advantage-weighted behavior cloning.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Fit an expectile value

For $u=Q_{\mathrm{target}}(s,a)-V(s)$,
$$L_V=\mathbb E_D[|\tau-\mathbf1[u<0]|u^2],\qquad \tau\in(0,1).$$
Choosing $\tau>1/2$ emphasizes higher-value dataset actions. An expectile is not a quantile; its residual penalty is quadratic.


**Implement this component:** [Compute an Expectile Regression Loss](/problems/iql-expectile-regression).


### Back up the critic

Fit
$$L_Q=\mathbb E_D[(Q(s,a)-r-\gamma(1-d)V(s'))^2].$$
Stop gradients through targets as required. $d$ denotes true termination; mishandling time-limit truncation biases the value estimate.


**Implement this component:** [Build IQL Critic Targets with Terminal Masks](/problems/soft-value-bellman-target). Shared one-step target arithmetic accepts supplied expectile values here; the SAC soft-value estimator itself is not reused.

**Implement this component:** [Validate an Offline Dataset Split](/problems/iql-offline-dataset-split).


### Extract an advantage-weighted policy

With advantage $A=Q_{\mathrm{target}}-V$, minimize
$$L_\pi=-\mathbb E_D[e^{\beta A(s,a)}\log\pi(a\mid s)].$$
Practical weights may be capped for stability. Larger $\beta$ concentrates on high-advantage samples; it does not create data for actions absent from the dataset.


**Implement this component:** [Build Advantage-Weighted Action Weights](/problems/iql-advantage-action-weights).


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Fit an expectile value:** [Compute an Expectile Regression Loss](/problems/iql-expectile-regression).
- **Back up the critic:** [Build IQL Critic Targets with Terminal Masks](/problems/soft-value-bellman-target); [Validate an Offline Dataset Split](/problems/iql-offline-dataset-split).
- **Extract an advantage-weighted policy:** [Build Advantage-Weighted Action Weights](/problems/iql-advantage-action-weights).

## Why this matters on a robot

IQL can exploit mixed-quality robot logs without direct online exploration during training. Poor action coverage and erroneous rewards still limit what its policy can learn.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2110.06169) · [Open-access manuscript](https://arxiv.org/pdf/2110.06169)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
