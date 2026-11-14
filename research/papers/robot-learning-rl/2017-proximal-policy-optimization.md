---
schema_version: 1
paper_id: 2017-proximal-policy-optimization
title: Proximal Policy Optimization Algorithms
authors:
  - 'Schulman, John'
  - 'Wolski, Filip'
  - 'Dhariwal, Prafulla'
  - 'Radford, Alec'
  - 'Klimov, Oleg'
year: 2017
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1707.06347'
pdf_url: 'https://arxiv.org/pdf/1707.06347'
local_pdf: ./2017-proximal-policy-optimization.pdf
sha256: e78feadadbdbb0b601b3c2bcc81404722cd431a489b307545f9b7bea1e8c4f5b
bytes: 2923532
pages: 12
topics:
  - robot-learning-rl
  - proximal-policy-optimization
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
      title: Collect advantages and old probabilities
      detail: Freeze the behavior policy for a rollout batch.
      column: 0
      row: 0
      section: Collect advantages and old probabilities
      problem_slugs:
        - ppo-normalize-batched-advantages
      planned_problems: []
    - id: stage-2
      title: Optimize the clipped surrogate
      detail: Limit the benefit of large policy-ratio changes.
      column: 1
      row: 0
      section: Optimize the clipped surrogate
      problem_slugs:
        - ppo-clipped-policy-surrogate
        - ppo-policy-update-clip-fractions
      planned_problems: []
    - id: stage-3
      title: Update value and collect again
      detail: 'Fit value targets, monitor policy change, and refresh experience.'
      column: 2
      row: 0
      section: Update value and collect again
      problem_slugs:
        - ppo-boundary-value-targets
      planned_problems: []
    - id: bounded-controller-integration
      title: Train and evaluate a bounded controller
      detail: >-
        Compose fixed-policy rollouts, terminal returns, clipped updates and
        held-out evaluation in a scalar synthetic joint environment.
      column: 3
      row: 0
      section: Bounded executable controller integration
      problem_slugs:
        - ppo-joint-controller-integration
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: rollout batch
    - from: stage-2
      to: stage-3
      label: updated policy
    - from: stage-3
      to: bounded-controller-integration
      label: reviewed update components
---

## Core paper explanation

PPO reuses a batch of on-policy experience for several optimization epochs while clipping the policy-ratio surrogate. The clipping discourages excessive improvement claims from large probability changes without imposing an exact trust-region constraint.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Collect advantages and old probabilities

For action $a_t$, retain $\log\pi_{\mathrm{old}}(a_t\mid s_t)$ and advantage estimate $\hat A_t$. Returns and advantages must respect terminal versus time-limit boundaries. Old log probabilities are fixed targets during the update.


**Implement this component:** [Normalize Batched Advantages](/problems/ppo-normalize-batched-advantages).


### Optimize the clipped surrogate

Define $r_t=\exp(\log\pi_\theta-\log\pi_{\mathrm{old}})$. Maximize
$$L^{\mathrm{clip}}=\mathbb E_t\min(r_t\hat A_t,\operatorname{clip}(r_t,1-\varepsilon,1+\varepsilon)\hat A_t).$$
The minimum handles positive and negative advantages differently. Clipping the ratio does not mean clipping gradients or guaranteeing a global KL bound.


**Implement this component:** [Compute the Clipped Policy Surrogate](/problems/ppo-clipped-policy-surrogate).

**Implement this component:** [Report Policy Update Clip Fractions](/problems/ppo-policy-update-clip-fractions).


### Update value and collect again

A value term commonly uses $(V_\theta(s_t)-\hat R_t)^2$, with entropy regularization encouraging exploration. Coefficients and any value clipping are implementation choices that must be declared. After bounded epochs, collect a new batch under the updated policy.


**Implement this component:** [Compute Value Targets Across Episode Boundaries](/problems/ppo-boundary-value-targets).


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Collect advantages and old probabilities:** [Normalize Batched Advantages](/problems/ppo-normalize-batched-advantages).
- **Optimize the clipped surrogate:** [Compute the Clipped Policy Surrogate](/problems/ppo-clipped-policy-surrogate); [Report Policy Update Clip Fractions](/problems/ppo-policy-update-clip-fractions).
- **Update value and collect again:** [Compute Value Targets Across Episode Boundaries](/problems/ppo-boundary-value-targets).

## Why this matters on a robot

PPO is convenient for parallel robot simulation. Stale data, incorrectly scaled continuous-action log probabilities, and reward exploitation can undermine training despite a well-behaved clipped loss.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1707.06347) · [Open-access manuscript](https://arxiv.org/pdf/1707.06347)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.

## Bounded executable controller integration

[Train and Evaluate a Tiny PPO Joint Controller](/problems/ppo-joint-controller-integration) runs an actual bounded policy-update loop: collect synthetic scalar-joint trajectories with supplied action noise, compute terminal discounted returns, normalize advantages, update a linear Gaussian policy over frozen rollout likelihoods and evaluate independent target positions. The [paper project](/projects/2017-proximal-policy-optimization) includes stage navigation, failure-analysis prompts and a reproducibility record.

This implements a small original environment and controller, not the paper’s neural locomotion experiments. It has no learned critic, neural perception, MuJoCo or real robot. Success means correct execution of the stated loop; improvement on arbitrary goals is not guaranteed.
