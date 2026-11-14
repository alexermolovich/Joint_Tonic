---
schema_version: 1
paper_id: 2018-soft-actor-critic
title: >-
  Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with
  a Stochastic Actor
authors:
  - 'Haarnoja, Tuomas'
  - 'Zhou, Aurick'
  - 'Abbeel, Pieter'
  - 'Levine, Sergey'
year: 2018
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1801.01290'
pdf_url: 'https://arxiv.org/pdf/1801.01290'
local_pdf: ./2018-soft-actor-critic.pdf
sha256: 5c33fae017d02f7025730f05198d4a6b103402822c8bbf48cbc5d8a0474c336a
bytes: 4388102
pages: 14
topics:
  - robot-learning-rl
  - soft-actor-critic
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
      title: Define entropy-regularized value
      detail: Reward both task performance and policy entropy.
      column: 0
      row: 0
      section: Define entropy-regularized value
      problem_slugs:
        - sac-soft-state-value
      planned_problems: []
    - id: stage-2
      title: Fit soft critic targets
      detail: Bootstrap from a target soft-value estimate.
      column: 1
      row: 0
      section: Fit soft critic targets
      problem_slugs:
        - soft-value-bellman-target
      planned_problems: []
    - id: stage-3
      title: Improve the stochastic actor
      detail: Trade high value against entropy using reparameterized actions.
      column: 2
      row: 0
      section: Improve the stochastic actor
      problem_slugs:
        - sac-tanh-logprob-correction
        - sac-temperature-objective-update
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: replay transitions
    - from: stage-2
      to: stage-3
      label: critic estimates
---

## Core paper explanation

Soft Actor-Critic learns a stochastic continuous-control policy with entropy-regularized value learning and off-policy replay. The original paper includes a separate soft value network; later SAC variants often eliminate it.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Define entropy-regularized value

With entropy coefficient $\alpha>0$,
$$V(s)=\mathbb E_{a\sim\pi}[Q(s,a)-\alpha\log\pi(a\mid s)].$$
The paper can absorb reward/entropy scale into its notation. Replay transitions allow learning from previously collected behavior rather than only the latest policy.


**Implement this component:** [Compute an Entropy-Regularized State Value](/problems/sac-soft-state-value).


### Fit soft critic targets

The original formulation uses
$$y=r+\gamma(1-d)V_{\mathrm{target}}(s'),\qquad L_Q=\tfrac12\mathbb E(Q(s,a)-y)^2.$$
$d$ marks true terminal transitions. The value network fits the soft expectation above; target-network averaging stabilizes bootstrapping.


**Implement this component:** [Compute an Entropy-Regularized Bellman Target](/problems/soft-value-bellman-target).


### Improve the stochastic actor

Minimize $L_\pi=\mathbb E[\alpha\log\pi(a\mid s)-Q(s,a)]$. For $a=\tanh(u)$, log density includes the Jacobian correction $-\sum_j\log(1-\tanh^2u_j)$. Action scaling and squashing must agree between sampling, critic inputs, and likelihoods.


**Implement this component:** [Apply Tanh Action Log-Probability Correction](/problems/sac-tanh-logprob-correction).

**Implement this component:** [Update a Temperature Objective (later SAC extension)](/problems/sac-temperature-objective-update).

**Related extension:** automatic temperature tuning belongs to the later [SAC Algorithms and Applications](https://arxiv.org/abs/1812.05905), rather than the original fixed-temperature formulation explained here. A future temperature exercise must cite that source and define its target-entropy convention.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Define entropy-regularized value:** [Compute an Entropy-Regularized State Value](/problems/sac-soft-state-value).
- **Fit soft critic targets:** [Compute an Entropy-Regularized Bellman Target](/problems/soft-value-bellman-target).
- **Improve the stochastic actor:** [Apply Tanh Action Log-Probability Correction](/problems/sac-tanh-logprob-correction); [Update a Temperature Objective (later SAC extension)](/problems/sac-temperature-objective-update).

## Why this matters on a robot

Replay improves sample reuse in costly robot interaction. Entropy encourages exploration but does not enforce physical safety; action bounds, controller behavior, and resets remain separate system responsibilities.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1801.01290) · [Open-access manuscript](https://arxiv.org/pdf/1801.01290)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
