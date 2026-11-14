---
schema_version: 1
paper_id: "2022-dexpoint"
title: "DexPoint: Generalizable Point Cloud Reinforcement Learning for Sim-to-Real Dexterous Manipulation"
authors: ["Qin, Yuzhe","Huang, Binghao","Yin, Zhao-Heng","Su, Hao","Wang, Xiaolong"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2211.09423"
pdf_url: "https://arxiv.org/pdf/2211.09423"
local_pdf: "./2022-dexpoint.pdf"
sha256: "c77516db0f09ad6c3964ee279b56c4db445502827af860fa3c1f5c7c517ae93d"
bytes: 6899060
pages: 13
topics: ["humanoid-dexterity-tactile","dexpoint"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Construct observed and imagined points","detail":"Combine object sensing with a kinematic hand representation.","column":0,"row":0,"section":"Construct observed and imagined points","problem_slugs":["se3-transform-points"],"planned_problems":["Merge Observed and Imagined Hand Point Clouds"]},{"id":"stage-2","title":"Learn contact-aware behavior","detail":"Use geometric features and contact-related reward shaping.","column":1,"row":0,"section":"Learn contact-aware behavior","problem_slugs":["pointnet-symmetric-pooling"],"planned_problems":["Compute a Contact-Based Manipulation Reward"]},{"id":"stage-3","title":"Transfer to new objects","detail":"Evaluate held-out geometry and real sensor observations.","column":2,"row":0,"section":"Transfer to new objects","problem_slugs":[],"planned_problems":["Evaluate Novel-Object Generalization"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"combined point cloud"},{"from":"stage-2","to":"stage-3","label":"trained policy"}]}
---

## Core paper explanation

DexPoint learns dexterous manipulation from point clouds and augments observations with imagined hand geometry from robot kinematics. Contact-aware rewards and geometric observations support transfer to unseen objects and real hardware.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Construct observed and imagined points

For sampled point $p_i^{L}$ on robot link $L$, imagined hand position is
$$p_i^B=T_{BL}(q)p_i^L.$$
Combine these points with observed scene points in the same base frame. Imagined geometry helps when the real hand is occluded, but it depends on accurate joint state and link models.


**Runnable component:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Transform sampled link points into a common frame; articulated forward kinematics and point fusion remain separate.

**Planned exercise:** Merge Observed and Imagined Hand Point Clouds.


### Learn contact-aware behavior

A point encoder aggregates the set into policy features. Contact-based rewards encourage useful hand–object interaction alongside task completion. A teaching geometric proximity is $d_i=\min_{p\in P_O}\|p_i^H-p\|_2$; distance alone is not a substitute for the paper's full contact reward or a physical force measurement.


**Runnable component:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). Practice the symmetric aggregation primitive; this does not implement the paper’s full encoder or contact reward.

**Planned exercise:** Compute a Contact-Based Manipulation Reward.


### Transfer to new objects

The training objective averages return across object instances and randomized conditions. Report success per unseen object and task, with fixed camera and hand calibration. A point-cloud input reduces some appearance differences but preserves depth noise, missing surfaces, and geometry mismatch.


**Planned exercise:** Evaluate Novel-Object Generalization.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Construct observed and imagined points:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points) (runnable component); Merge Observed and Imagined Hand Point Clouds (planned).
- **Learn contact-aware behavior:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling) (runnable component); Compute a Contact-Based Manipulation Reward (planned).
- **Transfer to new objects:** Evaluate Novel-Object Generalization (planned).

## Why this matters on a robot

Combining measured object points with kinematic hand geometry makes contact reasoning more explicit. Errors in the robot model or joint calibration can place the imagined fingers somewhere the real fingers are not.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2211.09423) · [Open-access manuscript](https://arxiv.org/pdf/2211.09423)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
