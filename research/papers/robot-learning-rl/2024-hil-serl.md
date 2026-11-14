---
schema_version: 1
paper_id: 2024-hil-serl
title: >-
  Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement
  Learning
authors:
  - 'Luo, Jianlan'
  - 'Xu, Charles'
  - 'Wu, Jeffrey'
  - 'Levine, Sergey'
year: 2024
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2410.21845'
pdf_url: 'https://arxiv.org/pdf/2410.21845'
local_pdf: ./2024-hil-serl.pdf
sha256: 547a4d5d9440a3f70a773798813db1c8a612f006a6994398bbee2a566daab526
bytes: 23020066
pages: 54
topics:
  - robot-learning-rl
  - hil-serl
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
      title: Collect policy and corrective actions
      detail: Let a human temporarily take control when behavior needs correction.
      column: 0
      row: 0
      section: Collect policy and corrective actions
      problem_slugs:
        - hilserl-intervention-segments
      planned_problems: []
    - id: stage-2
      title: Learn from mixed replay
      detail: Combine demonstration/correction evidence with online experience.
      column: 1
      row: 0
      section: Learn from mixed replay
      problem_slugs:
        - hilserl-mix-corrective-replay
      planned_problems: []
    - id: stage-3
      title: Update and evaluate autonomy
      detail: Distribute new policies and track success without assistance.
      column: 2
      row: 0
      section: Update and evaluate autonomy
      problem_slugs:
        - offline-rollout-checkpoint-gate
        - hilserl-autonomous-update-gate
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: labeled transitions
    - from: stage-2
      to: stage-3
      label: learner updates
---

## Core paper explanation

HIL-SERL combines real-robot off-policy reinforcement learning with human demonstrations and online corrective interventions. An actor, learner, replay storage, and learned success rewards form an integrated training system.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Collect policy and corrective actions

Record executed action $a_t$ and source label $h_t\in\{\mathrm{policy},\mathrm{human}\}$. When a human intervenes, the replay transition must contain the action actually sent to the controller, not the policy proposal that was overridden.


**Implement this component:** [Label Human Intervention Segments](/problems/hilserl-intervention-segments).


### Learn from mixed replay

Corrections must be stored as executed actions. Let $h_t\in\{0,1\}$ indicate human control, with proposed policy action $a_t^\pi$ and human action $a_t^H$ in the same D-dimensional controller coordinates. The logged transition uses

$$
a_t^{exec}=(1-h_t)a_t^\pi+h_t a_t^H,\qquad (s_t,a_t^{exec},r_t,s_{t+1},d_t).
$$

The binary terminal flag $d_t$ controls bootstrapping, not whether a human intervened. Under a chosen off-policy value target $V_{target}$, the scalar backup is

$$
y_t=r_t+\gamma(1-d_t)V_{target}(s_{t+1}).
$$

Gamma is the dimensionless discount. This equation illustrates replay bookkeeping; the actual learner supplies its critic ensemble, entropy terms and target-update details. If $a_t^\pi=[0.2,-0.1]$, $a_t^H=[0,0.3]$ and $h_t=1$, store [0,0.3]. With reward1,gamma0.9,target value2 and no terminal, backup2.8; if terminal, backup1. Human intervention alone must not set the terminal flag.

[Select a Checkpoint with Offline and Rollout Gates](/problems/offline-rollout-checkpoint-gate) is a related runnable evaluation gate. For this setting its rollout evidence must distinguish autonomous trials from assisted ones; the exercise does not implement HIL-SERL replay or intervention collection.

| Step | Policy proposal | Executed action | Logged source |
|---|---|---|---|
| autonomous | [0.2,-0.1] | [0.2,-0.1] | policy |
| intervention | [0.2,-0.1] | [0,0.3] | human |

This static trace makes source identity explicit and doubles as the text alternative.


A teaching replay mixture is $D_{\mathrm{batch}}\sim\eta D_{\mathrm{demo}}+(1-\eta)D_{\mathrm{online}}$. The actual system's buffer composition and sampling schedule must be retained. Critic targets use $y=r+\gamma(1-d)V_{\mathrm{target}}(s')$ under the chosen off-policy algorithm.


**Implement this component:** [Mix Intervention and Autonomous Replay](/problems/hilserl-mix-corrective-replay).

The exercise uses explicitly disjoint human and autonomous source pools with recorded priorities and half-up quotas. This is a reproducible teaching recipe; it does not assert that the paper's online and demonstration buffers are disjoint. Both the provenance label and the executed command survive sampling.


### Update and evaluate autonomy

A success classifier supplies task reward from observations. Classifier false positives can be exploited by the policy. Report autonomous success separately from training success with interventions, together with human time, interaction budget, and policy version.


**Implement this component:** [Gate an Online Policy Update](/problems/hilserl-autonomous-update-gate).

This original gate compares observed rates after removing assisted trials. Missing autonomous evidence fails the gate; the result provides neither a statistical confidence guarantee nor authorization to run hardware.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Collect policy and corrective actions:** [Label Human Intervention Segments](/problems/hilserl-intervention-segments).
- **Learn from mixed replay:** [Mix Intervention and Autonomous Replay](/problems/hilserl-mix-corrective-replay).
- **Update and evaluate autonomy:** [Gate an Online Policy Update](/problems/hilserl-autonomous-update-gate).

## Why this matters on a robot

Corrections can focus expensive experience on useful recovery behavior. Hidden human assistance or incorrect action-source logging can make a policy appear more autonomous than it is.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2410.21845) · [Open-access manuscript](https://arxiv.org/pdf/2410.21845)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
