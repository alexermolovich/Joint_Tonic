---
schema_version: 1
paper_id: "2021-dexmv"
title: "DexMV: Imitation Learning for Dexterous Manipulation from Human Videos"
authors: ["Qin, Yuzhe","Wu, Yueh-Hua","Liu, Shaowei","Jiang, Hanwen","Yang, Ruihan","Fu, Yang","Wang, Xiaolong"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2108.05877"
pdf_url: "https://arxiv.org/pdf/2108.05877"
local_pdf: "./2021-dexmv.pdf"
sha256: "9b2e0e5207253be4594aaf3dfca6db8d38527e937738239409e5536ef3cf57c4"
bytes: 8540406
pages: 25
topics: ["humanoid-dexterity-tactile","dexmv"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Estimate human and object motion","detail":"Recover temporally aligned hand and object geometry from video.","column":0,"row":0,"section":"Estimate human and object motion","problem_slugs":[],"planned_problems":["Map Human Demonstration Segments to Robot Time","Validate a Hand-Object Pose Sequence"]},{"id":"stage-2","title":"Retarget to robot kinematics","detail":"Match geometric relationships despite different hand morphology.","column":1,"row":0,"section":"Retarget to robot kinematics","problem_slugs":[],"planned_problems":["Compute a Hand-Retargeting Geometry Residual","Evaluate Retargeted Motion Feasibility"]},{"id":"stage-3","title":"Infer actions and learn","detail":"Turn retargeted states into robot control supervision.","column":2,"row":0,"section":"Infer actions and learn","problem_slugs":[],"planned_problems":["Validate Actions Inferred from Retargeted States"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"estimated poses"},{"from":"stage-2","to":"stage-3","label":"robot-state trajectory"}]}
---

## Core paper explanation

DexMV converts human manipulation videos into robot demonstrations by estimating hand/object pose, retargeting hand motion, and inferring robot actions. The inferred demonstrations then support imitation-augmented reinforcement learning in paired simulation tasks.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Estimate human and object motion

Pose estimates provide human hand keypoints $p_i^H(t)$ and object pose $T_{WO}(t)$. All observations must share a consistent metric scale and time reference. Occlusion errors propagate into later retargeting, so uncertainty should not disappear when producing a robot trajectory.


**Planned exercise:** Map Human Demonstration Segments to Robot Time.

**Planned exercise:** Validate a Hand-Object Pose Sequence.


### Retarget to robot kinematics

A schematic retargeting objective is
$$q^*=\arg\min_q\sum_iw_i\|v_i^R(q)-s\,v_i^H\|_2^2+\lambda\|q-q_{\mathrm{prev}}\|_2^2.$$
$v_i$ are selected hand vectors, $s$ handles scale, and joint limits constrain $q$. This summarizes geometric matching and temporal regularity; the exact paper objective uses its chosen keypoint relationships.


**Planned exercise:** Compute a Hand-Retargeting Geometry Residual.

**Planned exercise:** Evaluate Retargeted Motion Feasibility.


### Infer actions and learn

Robot actions must be estimated through the simulation/control model; differentiating positions alone does not determine contact torques. Demonstrations can supervise state-only imitation or state–action learning, depending on the algorithm. Evaluate whether inferred actions actually reproduce the intended object interaction.


**Planned exercise:** Validate Actions Inferred from Retargeted States.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Estimate human and object motion:** Map Human Demonstration Segments to Robot Time (planned); Validate a Hand-Object Pose Sequence (planned).
- **Retarget to robot kinematics:** Compute a Hand-Retargeting Geometry Residual (planned); Evaluate Retargeted Motion Feasibility (planned).
- **Infer actions and learn:** Validate Actions Inferred from Retargeted States (planned).

## Why this matters on a robot

Video expands access to dexterous demonstrations but leaves dynamics unobserved. Wrong contact timing, pose scale, or hand morphology mapping can produce visually similar yet physically impossible robot behavior.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2108.05877) · [Open-access manuscript](https://arxiv.org/pdf/2108.05877)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
