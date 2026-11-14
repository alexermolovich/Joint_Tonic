---
schema_version: 1
paper_id: "2021-loftr"
title: "LoFTR: Detector-Free Local Feature Matching with Transformers"
authors: ["Sun, Jiaming","Shen, Zehong","Wang, Yuang","Bao, Hujun","Zhou, Xiaowei"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2104.00680"
pdf_url: "https://arxiv.org/pdf/2104.00680"
local_pdf: "./2021-loftr.pdf"
sha256: "d2f18e76fd92f234362f72d01ecf99d37d144f488360aca809bdeefed7fd2cef"
bytes: 8175934
pages: 10
topics: ["geometry-calibration-slam","loftr"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Condition dense features","detail":"Use self-attention and cross-attention across image grids.","column":0,"row":0,"section":"Condition dense features","problem_slugs":[],"planned_problems":["Apply Paired-Image Self and Cross Attention"]},{"id":"stage-2","title":"Select coarse matches","detail":"Normalize pair similarities and retain confident mutual pairs.","column":1,"row":0,"section":"Select coarse matches","problem_slugs":[],"planned_problems":["Construct Coarse Correspondence Candidates"]},{"id":"stage-3","title":"Refine local positions","detail":"Estimate subpixel correspondence inside fine windows.","column":2,"row":0,"section":"Refine local positions","problem_slugs":[],"planned_problems":["Refine a Match in a Local Window","Filter Geometrically Inconsistent Matches"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"conditioned features"},{"from":"stage-2","to":"stage-3","label":"coarse pairs"}]}
---

## Core paper explanation

LoFTR finds image correspondences without first requiring a sparse keypoint detector. Transformer-conditioned coarse features identify candidate matches, and a fine-resolution stage refines their positions.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Condition dense features

Coarse feature grids become sequences $F_A\in\mathbb R^{N\times d}$ and $F_B\in\mathbb R^{M\times d}$ with positional encoding. Cross-attention lets a location in one image use evidence from the other before matching.




**Planned component problem:** Apply Paired-Image Self and Cross Attention. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Select coarse matches

For similarity $S_{ij}=f_i^\top g_j/\tau$, the dual-softmax option uses
$$P_{ij}=\operatorname{softmax}_{j}(S_{ij})\operatorname{softmax}_{i}(S_{ij}).$$
Thresholding and mutual consistency select coarse matches. The paper also investigates an optimal-transport matching alternative; these normalizations are different choices, not simultaneous requirements.


**Planned component problems:** Construct Coarse Correspondence Candidates. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Refine local positions

A local correlation distribution $p_k$ over fine-window offsets $\Delta u_k$ gives an expectation
$$\widehat{\Delta u}=\sum_k p_k\Delta u_k.$$
Map the refined coordinates back to original image pixels with the correct feature-grid scale. A confident local match still requires epipolar or pose verification for geometric use.


**Planned component problems:** Refine a Match in a Local Window; Filter Geometrically Inconsistent Matches. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

The stage-specific implementation ideas above are not runnable yet. A reviewed blueprint and evaluator are required before publication.

**Planned components:**

- Apply Paired-Image Self and Cross Attention.
- Construct Coarse Correspondence Candidates.
- Refine a Match in a Local Window.
- Filter Geometrically Inconsistent Matches.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Detector-free matching can help low-texture scenes. Repeated structures and moving objects can create coherent false matches; localization should combine matching evidence with robust geometry.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2104.00680) · [Open-access manuscript](https://arxiv.org/pdf/2104.00680)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
