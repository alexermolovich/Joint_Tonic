---
schema_version: 1
paper_id: "2019-superglue"
title: "SuperGlue: Learning Feature Matching with Graph Neural Networks"
authors: ["Sarlin, Paul-Edouard","DeTone, Daniel","Malisiewicz, Tomasz","Rabinovich, Andrew"]
year: 2019
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1911.11763"
pdf_url: "https://arxiv.org/pdf/1911.11763"
local_pdf: "./2019-superglue.pdf"
sha256: "ecda479b69be527724305cd748869f450fc635b9718d198e4e8c59a5ba8c5543"
bytes: 10312084
pages: 18
topics: ["geometry-calibration-slam","superglue"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Refine contextual descriptors","detail":"Alternate within-image and cross-image attention.","column":0,"row":0,"section":"Refine contextual descriptors","problem_slugs":[],"planned_problems":["Build a Feature-Matching Score Matrix"]},{"id":"stage-2","title":"Solve partial assignment","detail":"Include unmatched dustbins and normalize transport mass.","column":1,"row":0,"section":"Solve partial assignment","problem_slugs":[],"planned_problems":["Normalize Assignments with Sinkhorn Iterations","Reject Unmatched Features with Dustbins"]},{"id":"stage-3","title":"Extract and supervise matches","detail":"Keep confident mutual assignments and train unmatched outcomes.","column":2,"row":0,"section":"Extract and supervise matches","problem_slugs":[],"planned_problems":["Extract Mutual Matches and Unmatched Labels from Transport Scores"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"matching descriptors"},{"from":"stage-2","to":"stage-3","label":"transport matrix"}]}
---

## Core paper explanation

SuperGlue matches sparse keypoints by reasoning jointly about both images. An attentional graph network refines descriptors, then differentiable optimal transport produces a partial assignment that can leave points unmatched.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Refine contextual descriptors

Initial descriptors combine appearance with encoded position and detection score. Attention has the form $\operatorname{softmax}(QK^\top/\sqrt d)V$. Self-attention captures structure within one image; cross-attention compares evidence across images.


**Planned component problems:** Build a Feature-Matching Score Matrix. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Solve partial assignment

Scores $S_{ij}=f_i^\top g_j$ are augmented with a learned dustbin row and column. Entropic transport solves a softened assignment:
$$\max_{P\ge0}\langle S,P\rangle+\epsilon H(P),\qquad P\mathbf1=a,\quad P^\top\mathbf1=b.$$
The marginals include dustbin capacity; they are not simply uniform over the original keypoints. Sinkhorn iterations alternate row and column normalization.


**Planned component problems:** Normalize Assignments with Sinkhorn Iterations; Reject Unmatched Features with Dustbins. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Extract and supervise matches

Supervision minimizes negative log probability of ground-truth matches and appropriate dustbin assignments. At inference, confidence and mutual consistency filter correspondences. A many-to-one nearest-neighbor lookup is not equivalent to this partial-assignment layer.




**Planned component problem:** Extract Mutual Matches and Unmatched Labels from Transport Scores. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

## Implement the components

The stage-specific implementation ideas above are not runnable yet. A reviewed blueprint and evaluator are required before publication.

**Planned components:**

- Build a Feature-Matching Score Matrix.
- Normalize Assignments with Sinkhorn Iterations.
- Reject Unmatched Features with Dustbins.
- Extract Mutual Matches and Unmatched Labels from Transport Scores.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Context-aware matching helps reject ambiguous isolated features. Repeated patterns and incorrect training geometry can still generate coherent but wrong correspondences; downstream pose estimation needs geometric verification.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1911.11763) · [Open-access manuscript](https://arxiv.org/pdf/1911.11763)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
