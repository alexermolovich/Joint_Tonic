---
schema_version: 1
paper_id: 2023-dreamerv3
title: Mastering Diverse Domains through World Models
authors:
  - 'Hafner, Danijar'
  - 'Pasukonis, Jurgis'
  - 'Ba, Jimmy'
  - 'Lillicrap, Timothy'
year: 2023
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2301.04104'
pdf_url: 'https://arxiv.org/pdf/2301.04104'
local_pdf: ./2023-dreamerv3.pdf
sha256: d0385798e8bada8e81b915c1743be81d9ce8776f12ed937e09351995e099ce37
bytes: 2874717
pages: 40
topics:
  - robot-learning-rl
  - dreamerv3
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
      title: Learn latent dynamics
      detail: >-
        Combine recurrent state with stochastic posterior and prior
        representations.
      column: 0
      row: 0
      section: Learn latent dynamics
      problem_slugs:
        - dreamer-balanced-latent-loss
      planned_problems: []
    - id: stage-2
      title: Represent diverse target scales
      detail: Use signed logarithmic transforms and distributional targets.
      column: 1
      row: 0
      section: Represent diverse target scales
      problem_slugs:
        - dreamer-symlog-twohot-targets
      planned_problems: []
    - id: stage-3
      title: Improve behavior in imagination
      detail: Roll out latent states and train actor/critic from predicted returns.
      column: 2
      row: 0
      section: Improve behavior in imagination
      problem_slugs:
        - dreamer-continuation-lambda-returns
        - dreamer-imagined-latent-rollout
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: model predictions
    - from: stage-2
      to: stage-3
      label: trained world model
---

## Core paper explanation

DreamerV3 learns a latent world model from real experience and improves behavior using imagined trajectories. Scale-robust prediction and normalization choices help one configuration work across diverse task domains.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Learn latent dynamics

A recurrent state $h_t$ and stochastic state $z_t$ model observations. The prior $p(z_t\mid h_t)$ predicts without the current image; the posterior $q(z_t\mid h_t,x_t)$ uses it. KL terms with different stop-gradient placements train dynamics and representations, alongside reconstruction, reward, and continuation prediction.


**Implement this component:** [Compute a Balanced Latent-Model Loss](/problems/dreamer-balanced-latent-loss).


### Represent diverse target scales

The transforms are
$$\operatorname{symlog}(x)=\operatorname{sign}(x)\log(1+|x|),\quad \operatorname{symexp}(y)=\operatorname{sign}(y)(e^{|y|}-1).$$
Two-hot targets distribute mass between adjacent bins to represent continuous rewards/values. The precise bin locations and decoded expectation matter; this is not ordinary one-hot classification of rounded returns.


**Implement this component:** [Encode Symlog Two-Hot Reward Targets](/problems/dreamer-symlog-twohot-targets).


### Improve behavior in imagination

A lambda return has recursion $G_t^\lambda=r_t+\gamma c_t[(1-\lambda)V_{t+1}+\lambda G_{t+1}^\lambda]$, where $c_t$ is predicted continuation. The actor optimizes imagined outcomes while real interaction refreshes model data. World-model errors can compound beyond observed experience.


**Implement this component:** [Build Lambda-Return Targets](/problems/dreamer-continuation-lambda-returns).

**Implement this component:** [Roll Out Imagined Latent Trajectories](/problems/dreamer-imagined-latent-rollout).


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Learn latent dynamics:** [Compute a Balanced Latent-Model Loss](/problems/dreamer-balanced-latent-loss).
- **Represent diverse target scales:** [Encode Symlog Two-Hot Reward Targets](/problems/dreamer-symlog-twohot-targets).
- **Improve behavior in imagination:** [Build Lambda-Return Targets](/problems/dreamer-continuation-lambda-returns); [Roll Out Imagined Latent Trajectories](/problems/dreamer-imagined-latent-rollout).

## Why this matters on a robot

Imagination can reuse expensive robot observations efficiently. Incorrect contact dynamics or continuation predictions can produce attractive imagined plans that fail physically.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2301.04104) · [Open-access manuscript](https://arxiv.org/pdf/2301.04104)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
