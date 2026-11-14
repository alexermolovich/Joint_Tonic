---
schema_version: 1
paper_id: "2021-learning-to-walk-in-minutes"
title: "Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning"
authors: ["Rudin, Nikita","Hoeller, David","Reist, Philipp","Hutter, Marco"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2109.11978"
pdf_url: "https://arxiv.org/pdf/2109.11978"
local_pdf: "./2021-learning-to-walk-in-minutes.pdf"
sha256: "48014ee8af3e5a7fc26de2a5aac0de9ad593725075627c1a210d9d0f1e4ee62a"
bytes: 38462407
pages: 14
topics: ["humanoid-dexterity-tactile","learning-to-walk-in-minutes"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Collect parallel locomotion rollouts","detail":"Batch robot states, velocity commands, and actions on the GPU.","column":0,"row":0,"section":"Collect parallel locomotion rollouts","problem_slugs":[],"planned_problems":["Reset Failed Locomotion Environments"]},{"id":"stage-2","title":"Adapt terrain difficulty","detail":"Move each environment through a performance-based curriculum.","column":1,"row":0,"section":"Adapt terrain difficulty","problem_slugs":[],"planned_problems":["Sample Terrain Difficulty by Policy Progress"]},{"id":"stage-3","title":"Train and transfer control","detail":"Optimize locomotion rewards and validate the physical controller.","column":2,"row":0,"section":"Train and transfer control","problem_slugs":[],"planned_problems":["Compute Gait Tracking and Stability Metrics"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"episode outcomes"},{"from":"stage-2","to":"stage-3","label":"curriculum rollouts"}]}
---

## Core paper explanation

Learning to Walk in Minutes uses many GPU-parallel simulated quadrupeds and a terrain curriculum to accelerate locomotion training. The contribution includes adapting the learning setup to massive parallelism and transferring the resulting policy to a real robot.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Collect parallel locomotion rollouts

With $B$ environments and $T$ steps per rollout, a batch contains $BT$ transitions. Increasing $B$ while shrinking $T$ changes temporal credit assignment even at fixed batch size. State/reset masks must remain independent across robots.


**Planned exercise:** Reset Failed Locomotion Environments.


### Adapt terrain difficulty

A teaching curriculum state is $\ell_b\leftarrow\operatorname{clip}(\ell_b+\Delta_b,0,L_{\max})$, where $\Delta_b$ reflects progress/failure under the paper's terrain rules. The actual promotion criteria depend on traveled distance and commands, not an invented universal success threshold.


**Planned exercise:** Sample Terrain Difficulty by Policy Progress.


### Train and transfer control

A velocity-tracking reward can use $r_v=\exp(-\|v-v^*\|^2/\sigma)$, with $\sigma$ in squared velocity units. Additional terms penalize undesirable physical behavior. Joint targets pass through the robot's actuator/controller model; reported training time depends on hardware and parallelism.


**Planned exercise:** Compute Gait Tracking and Stability Metrics.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Collect parallel locomotion rollouts:** Reset Failed Locomotion Environments (planned).
- **Adapt terrain difficulty:** Sample Terrain Difficulty by Policy Progress (planned).
- **Train and transfer control:** Compute Gait Tracking and Stability Metrics (planned).

## Why this matters on a robot

Parallelism reduces wall-clock experimentation time. Simulator throughput does not guarantee transferable dynamics, and reward terms must be checked for unrealistic gait or actuator exploitation.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2109.11978) · [Open-access manuscript](https://arxiv.org/pdf/2109.11978)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
