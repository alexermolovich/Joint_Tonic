---
schema_version: 1
paper_id: "2022-peract"
title: "Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation"
authors: ["Shridhar, Mohit","Manuelli, Lucas","Fox, Dieter"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2209.05451"
pdf_url: "https://arxiv.org/pdf/2209.05451"
local_pdf: "./2022-peract.pdf"
sha256: "daab02c1ba8c47505f9eb54e8e61fd327e799bb20b392efd7f4d06b0357d0f17"
bytes: 8181953
pages: 28
topics: ["robot-learning-rl","peract"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Voxelize calibrated observations","detail":"Fuse RGB-D points into a bounded 3D workspace.","column":0,"row":0,"section":"Voxelize calibrated observations","problem_slugs":[],"planned_problems":["Voxelize a Calibrated RGB-D Scene"]},{"id":"stage-2","title":"Predict language-conditioned actions","detail":"Attend through a latent bottleneck and classify pose components.","column":1,"row":0,"section":"Predict language-conditioned actions","problem_slugs":[],"planned_problems":["Encode a Discrete Six-DoF Action Target"]},{"id":"stage-3","title":"Execute a keyframe target","detail":"Decode the pose and call the motion-planning interface.","column":2,"row":0,"section":"Execute a keyframe target","problem_slugs":[],"planned_problems":["Decode a Voxel Action Heatmap"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"voxel features"},{"from":"stage-2","to":"stage-3","label":"discrete action"}]}
---

## Core paper explanation

PerAct represents observations and translation actions in a voxel grid, conditions on language, and uses a Perceiver-style transformer to predict manipulation keyframes. A motion planner executes the resulting discretized pose and gripper commands.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Voxelize calibrated observations

For workspace minimum $b$ and voxel width $\Delta$, voxel index is
$$i=\left\lfloor(p-b)/\Delta\right\rfloor.$$
$p,b$ are in meters and the same frame. Reject out-of-bounds points rather than silently wrapping indices; voxel centers introduce finite translation precision.


**Planned exercise:** Voxelize a Calibrated RGB-D Scene.


### Predict language-conditioned actions

The network predicts translation voxel logits plus discretized rotation and gripper outputs. A schematic supervised objective is $L=L_{\mathrm{trans}}+L_{\mathrm{rot}}+L_{\mathrm{grip}}+L_{\mathrm{collision}}$, reflecting the model's action components. Each term has its own labels and output convention.


**Planned exercise:** Encode a Discrete Six-DoF Action Target.


### Execute a keyframe target

A voxel-center translation is $\hat p=b+\Delta(i+1/2)$. Rotation bin order and gripper state must follow the action codec. The collision-related output does not certify a collision-free path; the execution backend still checks feasibility.


**Planned exercise:** Decode a Voxel Action Heatmap.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Voxelize calibrated observations:** Voxelize a Calibrated RGB-D Scene (planned).
- **Predict language-conditioned actions:** Encode a Discrete Six-DoF Action Target (planned).
- **Execute a keyframe target:** Decode a Voxel Action Heatmap (planned).

## Why this matters on a robot

Voxel structure gives manipulation a useful 3D prior. Discretization, calibration error, and occluded geometry can make the selected keyframe infeasible despite confident classification.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2209.05451) · [Open-access manuscript](https://arxiv.org/pdf/2209.05451)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
