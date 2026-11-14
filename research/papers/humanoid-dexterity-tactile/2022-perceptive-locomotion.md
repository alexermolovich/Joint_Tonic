---
schema_version: 1
paper_id: "2022-perceptive-locomotion"
title: "Learning robust perceptive locomotion for quadrupedal robots in the wild"
authors: ["Miki, Takahiro","Lee, Joonho","Hwangbo, Jemin","Wellhausen, Lorenz","Koltun, Vladlen","Hutter, Marco"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2201.08117"
pdf_url: "https://arxiv.org/pdf/2201.08117"
local_pdf: "./2022-perceptive-locomotion.pdf"
sha256: "f54ecada187bd0599dad0452d63f462399d1df64a7713f5d1ad744eada3710c9"
bytes: 38674018
pages: 22
topics: ["humanoid-dexterity-tactile","perceptive-locomotion"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Train a privileged teacher","detail":"Learn locomotion with accurate terrain and environmental information.","column":0,"row":0,"section":"Train a privileged teacher","problem_slugs":[],"planned_problems":["Score a Privileged Terrain Teacher Rollout"]},{"id":"stage-2","title":"Learn a robust belief state","detail":"Fuse noisy exteroception with proprioceptive history.","column":1,"row":0,"section":"Learn a robust belief state","problem_slugs":[],"planned_problems":["Compute Belief Reconstruction and Teacher-Action Losses","Detect Stale Perception in a Control Window"]},{"id":"stage-3","title":"Deploy with onboard sensing","detail":"Predict joint targets from the learned belief and velocity command.","column":2,"row":0,"section":"Deploy with onboard sensing","problem_slugs":[],"planned_problems":["Align Terrain Samples to the Robot Frame","Evaluate Foot Clearance Across Terrain Slices"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"teacher targets and corrupted sensing"},{"from":"stage-2","to":"stage-3","label":"student policy"}]}
---

## Core paper explanation

Learning Robust Perceptive Locomotion combines proprioception and noisy terrain observations in a recurrent belief state. A privileged teacher learns in simulation, then a student learns to act using information available on the real robot.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Train a privileged teacher

The teacher policy is $a_t^T=\pi_T(o_t,e_t)$, where $e_t$ contains privileged simulation information. Ground-truth terrain, friction, and disturbances help train capable behavior but are not assumed observable at deployment.


**Planned exercise:** Score a Privileged Terrain Teacher Rollout.


### Learn a robust belief state

The student updates belief $b_t=F(b_{t-1},o_t^{\mathrm{prop}},o_t^{\mathrm{ext}})$ and minimizes an imitation/reconstruction objective of the form
$$L=\|a_t^S-a_t^T\|_2^2+\lambda\|\hat e_t-e_t\|_2^2.$$
This summarizes the two training purposes; individual reconstruction terms have their own scales. Gating lets the model reduce reliance on corrupted terrain information.


**Planned exercise:** Compute Belief Reconstruction and Teacher-Action Losses.

**Planned exercise:** Detect Stale Perception in a Control Window.


### Deploy with onboard sensing

Robot-centric elevation samples must use consistent frames, timestamps, and height units. The student outputs joint-position targets for the low-level controller. Sensor failure and terrain-map drift are tested through corruption regimes rather than assuming exteroception is always accurate.


**Planned exercise:** Align Terrain Samples to the Robot Frame.

**Planned exercise:** Evaluate Foot Clearance Across Terrain Slices.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Train a privileged teacher:** Score a Privileged Terrain Teacher Rollout (planned).
- **Learn a robust belief state:** Compute Belief Reconstruction and Teacher-Action Losses (planned); Detect Stale Perception in a Control Window (planned).
- **Deploy with onboard sensing:** Align Terrain Samples to the Robot Frame (planned); Evaluate Foot Clearance Across Terrain Slices (planned).

## Why this matters on a robot

Terrain preview helps choose footholds, while proprioception supports fallback when vision is unreliable. A plausible but displaced elevation map can be more dangerous than an explicit missing observation; confidence and timing matter.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2201.08117) · [Open-access manuscript](https://arxiv.org/pdf/2201.08117)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
