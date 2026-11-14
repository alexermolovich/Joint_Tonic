---
schema_version: 1
paper_id: "2024-depth-anything-v2"
title: "Depth Anything V2"
authors: ["Yang, Lihe","Kang, Bingyi","Huang, Zilong","Zhao, Zhen","Xu, Xiaogang","Feng, Jiashi","Zhao, Hengshuang"]
year: 2024
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2406.09414"
pdf_url: "https://arxiv.org/pdf/2406.09414"
local_pdf: "./2024-depth-anything-v2.pdf"
sha256: "b156a023aa9a5e33bda60489962af809a67e748797d4357c790d063739fed2d7"
bytes: 47749421
pages: 30
topics: ["perception-3d","depth-anything-v2"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Train a teacher with precise synthetic depth, produce real-image pseudo labels, and train/evaluate student depth models with the correct scale convention.","nodes":[{"id":"stage-1","title":"Learn from precise depth labels","detail":"Use reliable synthetic geometry to train sharp depth predictions.","column":0,"row":0,"section":"Learn from precise depth labels","problem_slugs":[],"planned_problems":["Mask invalid depth boundaries"]},{"id":"stage-2","title":"Create real-image supervision","detail":"Use the teacher to connect precise synthetic training to real visual distributions.","column":1,"row":0,"section":"Create real-image supervision","problem_slugs":[],"planned_problems":["Create Teacher Depth Targets with Validity and Preprocessing Metadata"]},{"id":"stage-3","title":"Evaluate depth and boundaries","detail":"Separate relative geometry, edge quality, and metric range accuracy.","column":2,"row":0,"section":"Evaluate depth and boundaries","problem_slugs":[],"planned_problems":["Align relative inverse-depth predictions","Evaluate metric error by distance and surface type"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"trained teacher"},{"from":"stage-2","to":"stage-3","label":"student predictions"}]}
---

## Core paper explanation

Depth Anything V2 improves monocular depth learning through high-quality synthetic supervision, a stronger teacher, and pseudo-labeled real images for student training. Its general relative-depth models predict affine-invariant inverse depth; metric-depth variants require additional metric supervision. The method’s data pipeline is therefore as important as its dense prediction architecture.

## Execution flow

Train a teacher with precise synthetic depth, produce real-image pseudo labels, and train/evaluate student depth models with the correct scale convention.

### Learn from precise depth labels

Let $d_i$ denote inverse depth at valid pixel $i$, and $\hat d_i$ a prediction. Affine ambiguity means equivalent relative predictions can differ by

$$
d'_i=s\hat d_i+t.
$$

The paper uses scale/shift-invariant and gradient-matching losses inherited from prior relative-depth work. A simple least-squares alignment used for explanation is $(s,t)=\arg\min\sum_{i\in\Omega}(s\hat d_i+t-d_i)^2$; it is not a claim that every training configuration uses this exact estimator.


**Planned component problems:** Mask invalid depth boundaries. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Create real-image supervision

Teacher predictions $\tilde d=f_T(I)$ become supervision for real image $I$. A confidence/validity mask $m_i$ restricts usable pixels:

$$
\mathcal L_{\mathrm{pseudo}}=\frac{\sum_i m_i\ell(\hat d_i,\tilde d_i)}{\sum_i m_i}.
$$

The paper removes high-loss regions of pseudo-labeled samples and uses feature alignment to preserve useful pretrained semantics. Masking must be tied to the defined criterion; a missing pixel must not become a supervised zero-depth value.




**Planned component problem:** Create Teacher Depth Targets with Validity and Preprocessing Metadata. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Evaluate depth and boundaries

A gradient diagnostic on residual $r_i=d'_i-d_i$ is

$$
\mathcal L_{\mathrm{grad}}=\sum_{i\in\Omega}\left(|\nabla_xr_i|+|\nabla_yr_i|\right),
$$

with differences evaluated only where neighboring pixels are valid. Sharp edges and low aligned relative error do not establish metric depth in meters. For metric deployment, use the metric model and report physical range error without per-image scale fitting.


**Planned component problems:** Align relative inverse-depth predictions; Evaluate metric error by distance and surface type. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

The stage-specific implementation ideas above are not runnable yet. A reviewed blueprint and evaluator are required before publication.

**Planned components:**

- Mask invalid depth boundaries.
- Create Teacher Depth Targets with Validity and Preprocessing Metadata.
- Align relative inverse-depth predictions.
- Evaluate metric error by distance and surface type.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Monocular scale ambiguity is critical when a depth map drives stopping distance or grasp reach. Pseudo labels can also preserve teacher failures on transparent or unusual surfaces. Keep relative and metric model variants, preprocessing, and evaluation protocols clearly separated.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2406.09414) · [Open-access manuscript](https://arxiv.org/pdf/2406.09414)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
