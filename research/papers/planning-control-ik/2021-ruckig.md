---
schema_version: 1
paper_id: 2021-ruckig
title: Jerk-limited Real-time Trajectory Generation with Arbitrary Target States
authors:
  - 'Berscheid, Lars'
  - 'Kröger, Torsten'
year: 2021
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2105.04830'
pdf_url: 'https://arxiv.org/pdf/2105.04830'
local_pdf: ./2021-ruckig.pdf
sha256: 6a91d1f505e7b842ca25f50df3f54e0ff6c8a43525a2ae4800a6b74cd62d3cff
bytes: 241901
pages: 9
topics:
  - planning-control-ik
  - ruckig
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
      title: Specify bounded endpoint states
      detail: 'Provide position, velocity, acceleration, and directional limits.'
      column: 0
      row: 0
      section: Specify bounded endpoint states
      problem_slugs:
        - trajectory-derivative-audit
      planned_problems: []
    - id: stage-2
      title: Integrate constant-jerk segments
      detail: Construct candidate switching profiles analytically.
      column: 1
      row: 0
      section: Integrate constant-jerk segments
      problem_slugs:
        - time-parameterized-trajectory
        - velocity-acceleration-command-limits
        - constant-jerk-segment
      planned_problems: []
    - id: stage-3
      title: Synchronize and sample
      detail: Choose a common feasible duration and evaluate each joint trajectory.
      column: 2
      row: 0
      section: Synchronize and sample
      problem_slugs: []
      planned_problems:
        - Synchronize Multi-Joint Motion Durations
  edges:
    - from: stage-1
      to: stage-2
      label: bounded states
    - from: stage-2
      to: stage-3
      label: candidate profiles
---

## Core paper explanation

Ruckig generates time-optimal state-to-state trajectories under velocity, acceleration, and jerk limits. It supports nonzero target velocity and acceleration and synchronizes multiple degrees of freedom.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Specify bounded endpoint states

For each joint, define initial and target $(q,\dot q,\ddot q)$ and bounds on velocity, acceleration, and jerk. Rotational units are radians, radians per second, radians per second squared, and radians per second cubed. Feasibility depends on endpoint derivatives, not only target position.


**Component practice**

- [Validate a Trajectory Against Derivative Limits](/problems/trajectory-derivative-audit) — runnable bounded component; see its documented scope.

### Integrate constant-jerk segments

Within duration $t$ and constant jerk $j$,
$$a(t)=a_0+jt,\quad v(t)=v_0+a_0t+\tfrac12jt^2,$$
$$q(t)=q_0+v_0t+\tfrac12a_0t^2+\tfrac16jt^3.$$
Ruckig searches valid profile structures and switching times rather than fitting an arbitrary cubic through endpoints.


**Component practice**

- [Integrate a Constant-Jerk Motion Segment](/problems/constant-jerk-segment) — runnable bounded component; see its documented scope.

In these scalar equations, $q_0,v_0,a_0$ are position, velocity, and acceleration at the segment start, $j$ is its constant jerk, and $t\ge0$ is elapsed time in seconds. For a rotational joint initially at rest with $j=2$ radians per second cubed and $t=0.5$ seconds, the end state is $a=1$ radian per second squared, $v=0.25$ radians per second, and $q=1/24\approx0.041667$ radians. Every joint has its own segment state; independent endpoint calculations do not establish synchronized feasibility.

[Interpolate a Time-Parameterized Trajectory](/problems/time-parameterized-trajectory) and [Enforce Velocity and Acceleration Limits](/problems/velocity-acceleration-command-limits) provide lower-order trajectory and command-bound practice. Their documented interpolation and clipping policies do not implement Ruckig's jerk-limited profile search or its time-optimality guarantee.


### Synchronize and sample

Independent minimum durations suggest a lower bound $T\ge\max_iT_i^{\min}$, but blocked duration intervals mean simply taking that maximum is not always sufficient. Synchronization selects a duration feasible for every joint. Sample the analytical trajectory using the actual controller period.


**Component practice**

- Synchronize Multi-Joint Motion Durations — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Runnable components and remaining ideas:**

- [Validate a Trajectory Against Derivative Limits](/problems/trajectory-derivative-audit) — runnable bounded component; see its documented scope.
- [Integrate a Constant-Jerk Motion Segment](/problems/constant-jerk-segment) — runnable bounded component; see its documented scope.
- Synchronize Multi-Joint Motion Durations — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Bounded jerk reduces abrupt acceleration changes during online replanning. Kinematic bounds do not automatically enforce actuator torque, contact, or obstacle constraints; those require additional models and checks.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2105.04830) · [Open-access manuscript](https://arxiv.org/pdf/2105.04830)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
