---
schema_version: 1
paper_id: "2018-deepmimic"
title: "DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills"
authors: ["Peng, Xue Bin","Abbeel, Pieter","Levine, Sergey","van de Panne, Michiel"]
year: 2018
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1804.02717"
pdf_url: "https://arxiv.org/pdf/1804.02717"
local_pdf: "./2018-deepmimic.pdf"
sha256: "4bd4cc353bd2dc19da99bb21a254cbfdb9840e49940ce69d484eb6d45bfa348f"
bytes: 7770304
pages: 18
topics: ["humanoid-dexterity-tactile","deepmimic"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Condition on reference phase","detail":"Provide physical state and the current reference-motion phase.","column":0,"row":0,"section":"Condition on reference phase","problem_slugs":[],"planned_problems":["Interpolate a Reference Motion Pose","Detect Phase Misalignment in a Motion Clip"]},{"id":"stage-2","title":"Measure imitation quality","detail":"Compare joint rotations, velocities, endpoints, and center of mass.","column":1,"row":0,"section":"Measure imitation quality","problem_slugs":[],"planned_problems":["Compute Pose and Velocity Imitation Rewards"]},{"id":"stage-3","title":"Optimize feedback control","detail":"Balance imitation with the requested task.","column":2,"row":0,"section":"Optimize feedback control","problem_slugs":[],"planned_problems":["Combine Imitation and Task Rewards for Motion Control"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"simulated motion"},{"from":"stage-2","to":"stage-3","label":"imitation and task rewards"}]}
---

## Core paper explanation

DeepMimic trains physically simulated characters to imitate reference motion while satisfying task objectives. Motion clips specify style and coordination, while reinforcement learning finds feedback actions that realize those motions under simulated dynamics.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Condition on reference phase

The policy receives state $s_t$, phase $\phi_t$, and optional task goal. Reference-state initialization samples starting states from the clip, exposing later motion segments without requiring the policy to reach them first. Early termination stops severely failed imitation rollouts.


**Planned exercise:** Interpolate a Reference Motion Pose.

**Planned exercise:** Detect Phase Misalignment in a Motion Clip.


### Measure imitation quality

A pose reward is
$$r_p=\exp\!\left[-2\sum_j\|\operatorname{Log}(R_j^{*\top}R_j)\|_2^2\right],$$
where rotation-vector errors are in radians. The imitation reward combines pose, velocity, end-effector, and center-of-mass terms. Their different units require the corresponding scale coefficients.


**Planned exercise:** Compute Pose and Velocity Imitation Rewards.


### Optimize feedback control

The overall reward takes the form $r=w_Ir_I+w_Gr_G$. A policy outputs targets to the character's control system rather than directly copying reference kinematics. Evaluate recovery from perturbations separately from matching an undisturbed clip.


**Planned exercise:** Combine Imitation and Task Rewards for Motion Control.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Condition on reference phase:** Interpolate a Reference Motion Pose (planned); Detect Phase Misalignment in a Motion Clip (planned).
- **Measure imitation quality:** Compute Pose and Velocity Imitation Rewards (planned).
- **Optimize feedback control:** Combine Imitation and Task Rewards for Motion Control (planned).

## Why this matters on a robot

Reference motion provides coordinated behavior that is difficult to hand-code. Human motion may exceed robot joint, torque, or contact limits; successful simulation imitation alone does not establish hardware feasibility.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1804.02717) · [Open-access manuscript](https://arxiv.org/pdf/1804.02717)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
