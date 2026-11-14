---
schema_version: 1
paper_id: "2024-3d-diffusion-policy"
title: "3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations"
authors: ["Ze, Yanjie","Zhang, Gu","Zhang, Kangning","Hu, Chenyuan","Wang, Muhan","Xu, Huazhe"]
year: 2024
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2403.03954"
pdf_url: "https://arxiv.org/pdf/2403.03954"
local_pdf: "./2024-3d-diffusion-policy.pdf"
sha256: "916ecb6011e5e311daa9a8ca53d0ec2d8f44f7d2034d9ba368de7102737d9682"
bytes: 14149153
pages: 17
topics: ["robot-learning-rl","3d-diffusion-policy"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Prepare sparse 3D observations","detail":"Crop and sample point clouds in a declared coordinate frame.","column":0,"row":0,"section":"Prepare sparse 3D observations","problem_slugs":["pointnet-symmetric-pooling","se3-transform-points"],"planned_problems":["Sample and Normalize Scene Points"]},{"id":"stage-2","title":"Train conditioned action diffusion","detail":"Predict corruption noise from point features and robot state.","column":1,"row":0,"section":"Train conditioned action diffusion","problem_slugs":["diffusion-action-noising","diffusion-conditional-noise-loss"],"planned_problems":["Condition an Action Denoiser on a Point Feature"]},{"id":"stage-3","title":"Sample and execute a chunk","detail":"Denoise actions and replan from new 3D observations.","column":2,"row":0,"section":"Sample and execute a chunk","problem_slugs":["diffusion-receding-horizon-window"],"planned_problems":["Evaluate Viewpoint and Geometry Shift"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"3D context"},{"from":"stage-2","to":"stage-3","label":"trained denoiser"}]}
---

## Core paper explanation

3D Diffusion Policy, or DP3, conditions action diffusion on a compact point-cloud representation and robot state. The central change is spatial observation encoding, not a replacement of the action diffusion principle.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Prepare sparse 3D observations

Points $P\in\mathbb R^{N\times3}$ are transformed into the policy frame before encoding. A compact point encoder aggregates per-point features, schematically $z=\max_i\phi(p_i)$. Workspace cropping, sampling, and normalization are part of the input contract, not incidental preprocessing.


**Runnable component:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). Implement the max-aggregation primitive after per-point features; sampling, normalization and encoder training remain separate.

**Runnable component:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move points into the declared policy frame before feature extraction.

**Planned exercise:** Sample and Normalize Scene Points.


### Train conditioned action diffusion

For normalized action chunk $A$,
$$A^k=\sqrt{\bar\alpha_k}A+\sqrt{1-\bar\alpha_k}\epsilon,\quad L=\mathbb E\|\epsilon-\epsilon_\theta(A^k,k,z,q)\|_F^2.$$
$q$ is robot state. Depth and action channels have different units before normalization.


**Runnable component:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising). Construct the forward corrupted action chunk with a supplied schedule and noise.

**Runnable component:** [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss). Evaluate masked epsilon-prediction error; conditioning features and the denoiser are supplied rather than learned here.

**Planned exercise:** Condition an Action Denoiser on a Point Feature.


### Sample and execute a chunk

Iterative reverse sampling generates a chunk; execute the configured prefix and refresh observations. Evaluate geometry, viewpoint, and appearance changes separately. The paper's empirical safety observations are not a formal guarantee for arbitrary robots or scenes.


**Runnable component:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window). Select a valid action-execution prefix; reverse diffusion and a robot controller are outside this exercise.

**Planned exercise:** Evaluate Viewpoint and Geometry Shift.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Prepare sparse 3D observations:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling) (runnable component); [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points) (runnable component); Sample and Normalize Scene Points (planned).
- **Train conditioned action diffusion:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising) (runnable component); [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss) (runnable component); Condition an Action Denoiser on a Point Feature (planned).
- **Sample and execute a chunk:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window) (runnable component); Evaluate Viewpoint and Geometry Shift (planned).

## Why this matters on a robot

Point clouds can reduce dependence on background appearance and expose spatial structure. Missing depth, reflective surfaces, and frame calibration errors can still remove or misplace critical geometry.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2403.03954) · [Open-access manuscript](https://arxiv.org/pdf/2403.03954)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
