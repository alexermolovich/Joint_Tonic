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
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Collect parallel locomotion rollouts","detail":"Batch robot states, velocity commands, and actions on the GPU.","column":0,"row":0,"section":"Collect parallel locomotion rollouts","problem_slugs":[],"planned_problems":["Reset Failed Locomotion Environments"]},{"id":"stage-2","title":"Adapt terrain difficulty","detail":"Move each environment through a performance-based curriculum.","column":1,"row":0,"section":"Adapt terrain difficulty","problem_slugs":[],"planned_problems":["Sample Terrain Difficulty by Policy Progress"]},{"id":"stage-3","title":"Train and transfer control","detail":"Optimize locomotion rewards and validate the physical controller.","column":2,"row":0,"section":"Train and transfer control","problem_slugs":["window-episode-without-crossing-boundaries","build-robot-sequence-validity-masks","mpc-tracking-cost"],"planned_problems":["Compute Gait Tracking and Stability Metrics"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"episode outcomes"},{"from":"stage-2","to":"stage-3","label":"curriculum rollouts"}]}
---

## Core paper explanation

Learning to Walk in Minutes uses many GPU-parallel simulated quadrupeds and a terrain curriculum to accelerate locomotion training. The contribution includes adapting the learning setup to massive parallelism and transferring the resulting policy to a real robot.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Collect parallel locomotion rollouts

With $B$ environments and $T$ steps per rollout, a batch contains $BT$ transitions. Increasing $B$ while shrinking $T$ changes temporal credit assignment even at fixed batch size. State/reset masks must remain independent across robots.


**Planned exercise:** Reset Failed Locomotion Environments.


### Adapt terrain difficulty

A teaching curriculum state is $\ell_b\leftarrow\operatorname{clip}(\ell_b+\Delta_b,0,L_{\max})$, where $\Delta_b$ reflects progress/failure under the paper's terrain rules. The actual promotion criteria depend on traveled distance and commands, not an invented universal success threshold. This clipping expression is a teaching approximation: the official implementation randomly reassigns an environment that passes the highest level instead of permanently clipping it there. Its promotion and demotion distances also depend on terrain length, commanded speed, and episode duration.


**Planned exercise:** Sample Terrain Difficulty by Policy Progress.


### Train and transfer control

#### Quantify command tracking before combining rewards

Let $\mathbf v_b,\mathbf v_b^*\in\mathbb R^2$ contain measured and commanded horizontal velocities in the same robot-base frame, both in meters per second, for environment $b\in\{1,\ldots,B\}$. With positive scale $\sigma_v$ in squared meters per squared second, define

$$
e_b=\|\mathbf v_b-\mathbf v_b^*\|_2^2,
\qquad r_{v,b}=\exp(-e_b/\sigma_v),
\qquad \bar r_v=\frac1B\sum_{b=1}^B r_{v,b}.
$$

The reward is dimensionless and lies in $(0,1]$ for finite errors. At command $(1,0)$ and measured velocity $(0.8,0.1)$ meters per second, $e_b=0.05$ and $\sigma_v=0.25$ gives $r_{v,b}=e^{-0.2}\approx0.818731$. A frame mismatch can reduce reward even when the robot follows the intended world trajectory. This horizontal tracking form matches the [official implementation's tracking term](https://github.com/leggedrobotics/legged_gym/blob/master/legged_gym/envs/base/legged_robot.py); its complete reward also contains other terms, weights, and time-step handling.

| Rollout quantity | Shape | Boundary rule |
| --- | --- | --- |
| Observation sequence | $B\times(T+1)\times d$ | $d$ state features; reset states belong to a new episode |
| Actions and rewards | $B\times T\times a$, $B\times T$ | $a$ action channels per control step |
| Episode identifiers | $B\times(T+1)$ | Never link a terminal state to another episode's start |

$T$ counts rollout steps, and each row represents a separate simulated robot. [Window an Episode Without Crossing Boundaries](/problems/window-episode-without-crossing-boundaries) and [Build Padding and Validity Masks for Robot Sequences](/problems/build-robot-sequence-validity-masks) implement these supporting data invariants. [Evaluate an MPC Tracking Cost](/problems/mpc-tracking-cost) practices a related quadratic tracking objective, not this exponential reward or the paper's PPO training algorithm. Simulator collection, policy optimization, and transfer validation remain distinct tasks.


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
