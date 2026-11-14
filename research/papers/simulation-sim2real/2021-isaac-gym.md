---
schema_version: 1
paper_id: 2021-isaac-gym
title: 'Isaac Gym: High Performance GPU-Based Physics Simulation For Robot Learning'
authors:
  - 'Makoviychuk, Viktor'
  - 'Wawrzyniak, Lukasz'
  - 'Guo, Yunrong'
  - 'Lu, Michelle'
  - 'Storey, Kier'
  - 'Macklin, Miles'
  - 'Hoeller, David'
  - 'Rudin, Nikita'
  - 'Allshire, Arthur'
  - 'Handa, Ankur'
  - 'State, Gavriel'
year: 2021
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2108.10470'
pdf_url: 'https://arxiv.org/pdf/2108.10470'
local_pdf: ./2021-isaac-gym.pdf
sha256: a2aa99541e7e9fc60daef471eaecf1bf1331485814f17da9fd5643804e475daa
bytes: 29187866
pages: 32
topics:
  - simulation-sim2real
  - isaac-gym
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
      title: Create parallel environments
      detail: Instantiate batched robots with explicit state indexing.
      column: 0
      row: 0
      section: Create parallel environments
      problem_slugs:
        - isaac-gym-batch-joint-state
      planned_problems: []
    - id: stage-2
      title: Step physics and policy on device
      detail: 'Keep observations, actions, and rollouts resident on the GPU.'
      column: 1
      row: 0
      section: Step physics and policy on device
      problem_slugs:
        - isaac-gym-steady-state-throughput
      planned_problems: []
    - id: stage-3
      title: Reset and train reproducibly
      detail: Apply per-environment resets and log randomized parameters.
      column: 2
      row: 0
      section: Reset and train reproducibly
      problem_slugs:
        - window-episode-without-crossing-boundaries
        - build-robot-sequence-validity-masks
        - simulator-selective-environment-reset
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: physics tensors
    - from: stage-2
      to: stage-3
      label: batched rollouts
---

## Core paper explanation

Isaac Gym keeps physics simulation and policy learning on the GPU, passing state through tensor interfaces instead of repeatedly moving data through the CPU. Its contribution is throughput-oriented simulation infrastructure, distinct from the later Isaac Sim product interface.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Create parallel environments

For $B$ environments and $J$ joints, a joint-state view may have shape $B\times J\times2$ for position and velocity. Actual flattened tensor layouts and actor indices must follow the API. Root pose, joint state, and rigid-body state are different buffers.


**Component practice**

- [Batch Independent Simulator States](/problems/isaac-gym-batch-joint-state).

### Step physics and policy on device

A useful timing model is $T_{\mathrm{iter}}=T_{\mathrm{physics}}+T_{\mathrm{policy}}+T_{\mathrm{learning}}+T_{\mathrm{sync}}$. This is a teaching profiling decomposition. Eliminating CPU transfers reduces one bottleneck but does not remove synchronization, rendering, or memory limits.


**Component practice**

- [Measure Simulation and Learning Throughput](/problems/isaac-gym-steady-state-throughput).

### Reset and train reproducibly

Reset mask $m_b$ selects which states return to initialized values; continuing environments must retain their trajectories. Store randomization distributions, simulator version, solver parameters, and control decimation. High samples per second is not equivalent to high sample efficiency.



<!-- joint-tonic-math-expansion -->
#### Reset only the environments that ended

For a teaching state buffer $X\in\mathbb R^{B\times D}$, reset states $X^0$ of the same shape, and boolean reset mask $m\in\{0,1\}^B$, masked replacement is

$$X'_{bd}=m_bX^0_{bd}+(1-m_b)X_{bd}.$$

This equation is a logical tensor operation, not an instruction to bypass Isaac Gym's documented state-buffer/update API. Each column retains its own declared physical unit. For two environments with rows $[1,2]$ and $[3,4]$, zero reset states and mask $[1,0]$, the output is $[0,0]$ and $[3,4]$. Resetting the whole batch would erase the continuing trajectory.

Control interval is $\Delta t_{\mathrm{control}}=d\Delta t_{\mathrm{physics}}$ for integer decimation $d\ge1$, both times in seconds. With 0.002-second physics steps and d=5, control updates occur every 0.01 seconds. [Episode-boundary windows](/problems/window-episode-without-crossing-boundaries) and [validity masks](/problems/build-robot-sequence-validity-masks) preserve reset boundaries in training data; they are not a GPU simulator integration.
<!-- /joint-tonic-math-expansion -->

**Component practice**

- [Reset Completed Environments Selectively](/problems/simulator-selective-environment-reset).

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Component status:**

- [Batch Independent Simulator States](/problems/isaac-gym-batch-joint-state).
- [Measure Simulation and Learning Throughput](/problems/isaac-gym-steady-state-throughput).
- [Reset Completed Environments Selectively](/problems/simulator-selective-environment-reset).

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Scope of the runnable components

The exercises gather explicitly indexed revolute-joint states, reset selected rows and counters, and aggregate serialized timing evidence. Joint indices must be globally unique across the selected environments. Throughput counts supplied environment steps once and excludes declared warmup; it is not an asynchronous GPU benchmark or simulator API implementation.

## Why this matters on a robot

GPU rollouts make large-scale policy training accessible. Correlated environments, incorrect reset masks, and unrealistic contact settings can produce many low-value samples quickly.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2108.10470) · [Open-access manuscript](https://arxiv.org/pdf/2108.10470)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
