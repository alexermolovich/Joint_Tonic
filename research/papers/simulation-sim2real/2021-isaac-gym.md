---
schema_version: 1
paper_id: "2021-isaac-gym"
title: "Isaac Gym: High Performance GPU-Based Physics Simulation For Robot Learning"
authors: ["Makoviychuk, Viktor","Wawrzyniak, Lukasz","Guo, Yunrong","Lu, Michelle","Storey, Kier","Macklin, Miles","Hoeller, David","Rudin, Nikita","Allshire, Arthur","Handa, Ankur","State, Gavriel"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2108.10470"
pdf_url: "https://arxiv.org/pdf/2108.10470"
local_pdf: "./2021-isaac-gym.pdf"
sha256: "a2aa99541e7e9fc60daef471eaecf1bf1331485814f17da9fd5643804e475daa"
bytes: 29187866
pages: 32
topics: ["simulation-sim2real","isaac-gym"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Create parallel environments","detail":"Instantiate batched robots with explicit state indexing.","column":0,"row":0,"section":"Create parallel environments","problem_slugs":[],"planned_problems":["Batch Independent Simulator States"]},{"id":"stage-2","title":"Step physics and policy on device","detail":"Keep observations, actions, and rollouts resident on the GPU.","column":1,"row":0,"section":"Step physics and policy on device","problem_slugs":[],"planned_problems":["Measure Simulation and Learning Throughput"]},{"id":"stage-3","title":"Reset and train reproducibly","detail":"Apply per-environment resets and log randomized parameters.","column":2,"row":0,"section":"Reset and train reproducibly","problem_slugs":[],"planned_problems":["Reset Completed Environments Selectively"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"physics tensors"},{"from":"stage-2","to":"stage-3","label":"batched rollouts"}]}
---

## Core paper explanation

Isaac Gym keeps physics simulation and policy learning on the GPU, passing state through tensor interfaces instead of repeatedly moving data through the CPU. Its contribution is throughput-oriented simulation infrastructure, distinct from the later Isaac Sim product interface.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Create parallel environments

For $B$ environments and $J$ joints, a joint-state view may have shape $B\times J\times2$ for position and velocity. Actual flattened tensor layouts and actor indices must follow the API. Root pose, joint state, and rigid-body state are different buffers.


**Component practice**

- Batch Independent Simulator States — unreviewed idea; contract and evaluator required.

### Step physics and policy on device

A useful timing model is $T_{\mathrm{iter}}=T_{\mathrm{physics}}+T_{\mathrm{policy}}+T_{\mathrm{learning}}+T_{\mathrm{sync}}$. This is a teaching profiling decomposition. Eliminating CPU transfers reduces one bottleneck but does not remove synchronization, rendering, or memory limits.


**Component practice**

- Measure Simulation and Learning Throughput — unreviewed idea; contract and evaluator required.

### Reset and train reproducibly

Reset mask $m_b$ selects which states return to initialized values; continuing environments must retain their trajectories. Store randomization distributions, simulator version, solver parameters, and control decimation. High samples per second is not equivalent to high sample efficiency.


**Component practice**

- Reset Completed Environments Selectively — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Batch Independent Simulator States — unreviewed idea; contract and evaluator required.
- Measure Simulation and Learning Throughput — unreviewed idea; contract and evaluator required.
- Reset Completed Environments Selectively — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

GPU rollouts make large-scale policy training accessible. Correlated environments, incorrect reset masks, and unrealistic contact settings can produce many low-value samples quickly.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2108.10470) · [Open-access manuscript](https://arxiv.org/pdf/2108.10470)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
