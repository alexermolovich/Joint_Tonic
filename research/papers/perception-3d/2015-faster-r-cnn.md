---
schema_version: 1
paper_id: "2015-faster-r-cnn"
title: "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks"
authors: ["Ren, Shaoqing","He, Kaiming","Girshick, Ross","Sun, Jian"]
year: 2015
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1506.01497"
pdf_url: "https://arxiv.org/pdf/1506.01497"
local_pdf: "./2015-faster-r-cnn.pdf"
sha256: "f2630182ccfabd6fc89ac20270b4daf15a0ca849298a7db1e5d124ca443051f1"
bytes: 6913803
pages: 14
topics: ["perception-3d","faster-r-cnn"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Shared image features generate anchor-based proposals, proposals are filtered into regions of interest, and a second head predicts their final classes and boxes.","nodes":[{"id":"stage-1","title":"Encode anchor targets","detail":"Represent target boxes as offsets relative to an anchor’s center and size.","column":0,"row":0,"section":"Encode anchor targets","problem_slugs":[],"planned_problems":["Generate dense anchors","Encode and decode proposal regression targets"]},{"id":"stage-2","title":"Select region proposals","detail":"Use foreground scores, box decoding, clipping, and duplicate removal.","column":1,"row":0,"section":"Select region proposals","problem_slugs":["box-iou-broadcast","class-aware-nms"],"planned_problems":["Filter proposals and test region-feature alignment"]},{"id":"stage-3","title":"Classify and refine regions","detail":"Convert variable regions into fixed-size features for a second prediction head.","column":2,"row":0,"section":"Classify and refine regions","problem_slugs":[],"planned_problems":["Pool Proposal Regions and Apply Class-Specific Box Deltas"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"anchor predictions"},{"from":"stage-2","to":"stage-3","label":"regions of interest"}]}
---

## Core paper explanation

Faster R-CNN uses a region-proposal network to suggest object regions from shared image features, then a second stage classifies and refines those regions. Sharing the feature backbone avoids running a separate expensive proposal system. The two-stage design creates clear implementation boundaries: anchors and regression targets, proposal filtering, and region-based prediction.

## Execution flow

Shared image features generate anchor-based proposals, proposals are filtered into regions of interest, and a second head predicts their final classes and boxes.

### Encode anchor targets

For anchor $(x_a,y_a,w_a,h_a)$ and target $(x,y,w,h)$ in the same image coordinates,

$$
t_x=(x-x_a)/w_a,\quad t_y=(y-y_a)/h_a,
\quad t_w=\log(w/w_a),\quad t_h=\log(h/h_a).
$$

The offsets are dimensionless. Anchors need positive width and height, and anchor enumeration order must agree with the prediction tensor. Decode with $x=x_a+w_at_x$ and $w=w_ae^{t_w}$, with analogous vertical terms.


**Planned component problems:** Generate dense anchors; Encode and decode proposal regression targets. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Select region proposals

The proposal objective combines classification and regression over suitable anchors:

$$
\mathcal L_{\mathrm{RPN}}=\frac1{N_c}\sum_i\mathcal L_{\mathrm{cls}}(p_i,p_i^*)
+\frac{\lambda}{N_r}\sum_i p_i^*\mathcal L_{\mathrm{reg}}(t_i,t_i^*).
$$

Only positive anchors contribute regression targets. [IoU](/problems/box-iou-broadcast) supports matching and overlap checks. [NMS](/problems/class-aware-nms) provides the duplicate-removal mechanism, although the proposal stage uses foreground proposals rather than final semantic classes.


**Implement this component:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast) · [Run Class-Aware Non-Maximum Suppression](/problems/class-aware-nms). Use the suppression primitive with one class for class-agnostic proposals; proposal scoring, regression and region extraction remain separate.

**Planned component problems:** Filter proposals and test region-feature alignment. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Classify and refine regions

Region-of-interest pooling produces a fixed feature shape for every proposal. A head predicts class probabilities and an additional box correction. A typical robust coordinate penalty is

$$
\operatorname{smoothL1}(x)=\begin{cases}\tfrac12x^2,&|x|<1,\\|x|-\tfrac12,&|x|\ge1.\end{cases}
$$

Quantized pooling regions can lose spatial precision; this limitation later motivates ROIAlign in Mask R-CNN. Keep the first-stage and second-stage regression reference boxes distinct.




**Planned component problem:** Pool Proposal Regions and Apply Class-Specific Box Deltas. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

## Implement the components

- **Related implementation skill:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Run Class-Aware Non-Maximum Suppression](/problems/class-aware-nms). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Generate dense anchors.
- Encode and decode proposal regression targets.
- Filter proposals and test region-feature alignment.
- Pool Proposal Regions and Apply Class-Specific Box Deltas.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Two-stage refinement can improve localization, but it adds proposal-count and latency tradeoffs. Invalid anchor ordering or resize transforms can corrupt every final box. Benchmark crowded scenes and proposal truncation, not only isolated objects.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1506.01497) · [Open-access manuscript](https://arxiv.org/pdf/1506.01497)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
