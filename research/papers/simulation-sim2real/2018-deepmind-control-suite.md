---
schema_version: 1
paper_id: 2018-deepmind-control-suite
title: DeepMind Control Suite
authors:
  - 'Tassa, Yuval'
  - 'Doron, Yotam'
  - 'Muldal, Alistair'
  - 'Erez, Tom'
  - 'Li, Yazhe'
  - 'Casas, Diego de Las'
  - 'Budden, David'
  - 'Abdolmaleki, Abbas'
  - 'Merel, Josh'
  - 'Lefrancq, Andrew'
  - 'Lillicrap, Timothy'
  - 'Riedmiller, Martin'
year: 2018
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1801.00690'
pdf_url: 'https://arxiv.org/pdf/1801.00690'
local_pdf: ./2018-deepmind-control-suite.pdf
sha256: cdd89fa0165267b7a248ff694a578bee58df12293cdcafebf6918cb241160377
bytes: 6697782
pages: 24
topics:
  - simulation-sim2real
  - deepmind-control-suite
modalities:
  - simulator-state
  - robot-actions
  - sensor-observations
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
      title: Configure dynamics and observations
      detail: 'Declare state, actuators, timestep, and task inputs.'
      column: 0
      row: 0
      section: Configure dynamics and observations
      problem_slugs:
        - dm-control-timestep-validation
        - dm-control-action-repeat
      planned_problems: []
    - id: stage-2
      title: Compute interpretable reward
      detail: Map task variables into bounded tolerance-based scores.
      column: 1
      row: 0
      section: Compute interpretable reward
      problem_slugs:
        - dm-control-tolerance-reward
      planned_problems: []
    - id: stage-3
      title: Compare learning runs
      detail: Report returns under fixed evaluation and seed conventions.
      column: 2
      row: 0
      section: Compare learning runs
      problem_slugs:
        - dm-control-seeded-return-summary
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: simulated state
    - from: stage-2
      to: stage-3
      label: episode rewards
---

## Core paper explanation

The DeepMind Control Suite standardizes continuous-control environments with interpretable rewards and MuJoCo dynamics. It separates physical state, observations, task reward, and episode semantics so learning algorithms can be compared consistently.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Configure dynamics and observations

Mechanical dynamics follow a form such as
$$M(q)\ddot q+C(q,\dot q)+g(q)=\tau+J^\top f_c.$$
$q$ is configuration, $\tau$ actuator torque, and $f_c$ contact force. This is background mechanics; the simulator implements its own numerical solver and actuator models. The policy observation can omit parts of the full physical state.


**Component practice**

- [Validate a Continuous-Control Time Step](/problems/dm-control-timestep-validation).
- [Implement Action Repeat Correctly](/problems/dm-control-action-repeat).

### Compute interpretable reward

A tolerance function is one inside a desired interval and decreases smoothly outside it. A teaching form is $r(x)=1$ for $x\in[l,u]$, otherwise $r(x)=g(d(x,[l,u])/m)$, where $m$ is a margin and $g$ the chosen decay. Different tasks compose these terms differently.


**Component practice**

- [Evaluate a Bounded Continuous-Control Reward](/problems/dm-control-tolerance-reward).

### Compare learning runs

Return is $G=\sum_{t=0}^{T-1}\gamma^tr_t$ for declared discount $\gamma$. Evaluation summaries must specify whether they use discounted or undiscounted return. Keep control frequency, horizon, and termination/truncation conventions fixed across algorithms.


**Component practice**

- [Aggregate Seeded Benchmark Returns](/problems/dm-control-seeded-return-summary).

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Component status:**

- [Validate a Continuous-Control Time Step](/problems/dm-control-timestep-validation).
- [Implement Action Repeat Correctly](/problems/dm-control-action-repeat).
- [Evaluate a Bounded Continuous-Control Reward](/problems/dm-control-tolerance-reward).
- [Aggregate Seeded Benchmark Returns](/problems/dm-control-seeded-return-summary).

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Scope of the runnable components

The time-step validator permits a nonzero LAST discount for a truncated episode; action repeat consumes the LAST transition before stopping. The reward exercise isolates Gaussian tolerance, and the return summary averages episodes within seeds and then seeds within tasks. These components neither run dm_control nor claim one universal task reward or benchmark protocol.

## Why this matters on a robot

Standardized tasks help isolate learning behavior. Good simulator return does not prove robustness to real sensor delay, actuator dynamics, or contact uncertainty.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1801.00690) · [Open-access manuscript](https://arxiv.org/pdf/1801.00690)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
