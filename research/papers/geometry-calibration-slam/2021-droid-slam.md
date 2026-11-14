---
schema_version: 1
paper_id: "2021-droid-slam"
title: "DROID-SLAM: Deep Visual SLAM for Monocular, Stereo, and RGB-D Cameras"
authors: ["Teed, Zachary","Deng, Jia"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2108.10869"
pdf_url: "https://arxiv.org/pdf/2108.10869"
local_pdf: "./2021-droid-slam.pdf"
sha256: "0e15f20bff5f7ceac468c2899baafc8c114a3018c7a7b213eed7c402e5ccec90"
bytes: 11003883
pages: 15
topics: ["geometry-calibration-slam","droid-slam"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Project dense correspondences","detail":"Use current poses and depths to relate image pixels.","column":0,"row":0,"section":"Project dense correspondences","problem_slugs":[],"planned_problems":["Build a Dense Reprojection Residual"]},{"id":"stage-2","title":"Predict correspondence updates","detail":"Use a recurrent network to refine targets and confidence.","column":1,"row":0,"section":"Predict correspondence updates","problem_slugs":[],"planned_problems":["Apply Recurrent Dense Correspondence and Confidence Updates"]},{"id":"stage-3","title":"Run dense bundle adjustment","detail":"Jointly solve for pose and inverse-depth changes.","column":2,"row":0,"section":"Run dense bundle adjustment","problem_slugs":[],"planned_problems":["Select Edges for a Frame Graph","Update Poses in a Small Bundle-Adjustment Problem"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"correlation features"},{"from":"stage-2","to":"stage-3","label":"targets and weights"}]}
---

## Core paper explanation

DROID-SLAM alternates learned correspondence refinement with a differentiable dense bundle-adjustment layer. The network predicts correspondence corrections and confidence while geometric optimization jointly updates camera poses and inverse depths.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Project dense correspondences

For pixel $u_i$, inverse depth $d_i$, and relative pose $T_{ji}$,
$$u_{ij}=\pi(T_{ji}\pi^{-1}(u_i,d_i)).$$
Features and correlation volumes provide visual evidence around these current geometric predictions.


**Prerequisite practice:** [Project Camera Points into Pixels](/problems/project-camera-points). These supporting skills do not complete this model stage.

**Planned component problems:** Build a Dense Reprojection Residual. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Predict correspondence updates

The recurrent update predicts target corrections $\delta_{ij}$ and weights $w_{ij}$. Set $\hat u_{ij}=u_{ij}+\delta_{ij}$. Weights express how strongly the geometric solve should trust each correspondence; they do not automatically constitute calibrated physical uncertainty.




**Planned component problem:** Apply Recurrent Dense Correspondence and Confidence Updates. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Run dense bundle adjustment

The dense objective is
$$E(T,d)=\sum_{ij}\|\hat u_{ij}-\pi(T_{ji}\pi^{-1}(u_i,d_i))\|_{w_{ij}}^2.$$
Linearization and a Schur complement exploit the pose/depth structure. Recurrent updates repeat with improved geometry. Stereo or RGB-D measurements can constrain scale at inference; monocular geometry retains its gauge ambiguity.


**Planned component problems:** Select Edges for a Frame Graph; Update Poses in a Small Bundle-Adjustment Problem. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Project Camera Points into Pixels](/problems/project-camera-points). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Build a Dense Reprojection Residual.
- Apply Recurrent Dense Correspondence and Confidence Updates.
- Select Edges for a Frame Graph.
- Update Poses in a Small Bundle-Adjustment Problem.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Learned matching and explicit geometry can complement each other. Dynamic objects, disconnected frame graphs, and poor depth initialization can still break tracking; monitor residuals and connectivity rather than only network confidence.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2108.10869) · [Open-access manuscript](https://arxiv.org/pdf/2108.10869)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
