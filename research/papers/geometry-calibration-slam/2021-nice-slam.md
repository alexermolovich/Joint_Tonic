---
schema_version: 1
paper_id: "2021-nice-slam"
title: "NICE-SLAM: Neural Implicit Scalable Encoding for SLAM"
authors: ["Zhu, Zihan","Peng, Songyou","Larsson, Viktor","Xu, Weiwei","Bao, Hujun","Cui, Zhaopeng","Oswald, Martin R.","Pollefeys, Marc"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2112.12130"
pdf_url: "https://arxiv.org/pdf/2112.12130"
local_pdf: "./2021-nice-slam.pdf"
sha256: "734cc95a355c07c035696ef7610161522a64af4e9f86d99c2ab3eb1154eb05c6"
bytes: 27574309
pages: 17
topics: ["geometry-calibration-slam","nice-slam"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Interpolate hierarchical features","detail":"Query local grids at multiple spatial resolutions.","column":0,"row":0,"section":"Interpolate hierarchical features","problem_slugs":[],"planned_problems":["Query Multi-Resolution Scene Features"]},{"id":"stage-2","title":"Decode occupancy and color","detail":"Combine coarse structure with local geometric detail.","column":1,"row":0,"section":"Decode occupancy and color","problem_slugs":[],"planned_problems":["Decode Occupancy and Color from Hierarchical Scene Features"]},{"id":"stage-3","title":"Optimize tracking and mapping","detail":"Use rendered depth and color against RGB-D measurements.","column":2,"row":0,"section":"Optimize tracking and mapping","problem_slugs":[],"planned_problems":["Sample Rays for Online Mapping","Measure Pose and Reconstruction Error"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"interpolated features"},{"from":"stage-2","to":"stage-3","label":"rendered rays"}]}
---

## Core paper explanation

NICE-SLAM uses hierarchical local feature grids and pretrained geometric decoders for neural RGB-D mapping. Local features improve scalability compared with storing an entire scene only in one global network.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Interpolate hierarchical features

For world point $x$, trilinear interpolation gives
$$f_\ell(x)=\sum_{v\in\mathcal N_\ell(x)}w_v(x)F_{\ell,v},\qquad\sum_vw_v(x)=1.$$
$\ell$ identifies a grid level, $F_{\ell,v}$ a learned feature vector, and $\mathcal N_\ell(x)$ the eight neighboring grid vertices. Grid coordinates must be derived from metric world bounds.


**Planned component problems:** Query Multi-Resolution Scene Features. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Decode occupancy and color

Pretrained decoders turn hierarchical features into occupancy estimates, with finer levels refining geometry. Color uses its own representation. For occupancy probabilities $o_k$ along a ray, rendering weights follow
$$w_k=o_k\prod_{j<k}(1-o_j).$$
This occupancy formulation differs from treating the decoder output as unbounded NeRF volume density.




**Planned component problem:** Decode Occupancy and Color from Hierarchical Scene Features. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Optimize tracking and mapping

Predicted depth is $\hat D=\sum_k w_kt_k$, with ray depths $t_k$ in meters. Tracking updates camera pose; mapping updates relevant grid features and selected keyframe poses using geometric and photometric residuals. Coarse geometry provides support before fine detail is fully observed.


**Planned component problems:** Sample Rays for Online Mapping; Measure Pose and Reconstruction Error. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Project Camera Points into Pixels](/problems/project-camera-points). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Query Multi-Resolution Scene Features.
- Decode Occupancy and Color from Hierarchical Scene Features.
- Sample Rays for Online Mapping.
- Measure Pose and Reconstruction Error.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Hierarchical mapping can preserve detail over larger interiors. Occlusions, dynamic objects, and unsupported occupancy predictions still matter; a smooth reconstructed surface is not automatically a reliable contact surface.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2112.12130) · [Open-access manuscript](https://arxiv.org/pdf/2112.12130)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
