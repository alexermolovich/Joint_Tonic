---
schema_version: 1
paper_id: "2017-mask-r-cnn"
title: "Mask R-CNN"
authors: ["He, Kaiming","Gkioxari, Georgia","Dollár, Piotr","Girshick, Ross"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1703.06870"
pdf_url: "https://arxiv.org/pdf/1703.06870"
local_pdf: "./2017-mask-r-cnn.pdf"
sha256: "b595a882b763d55d933543131f32a2c4b6f41d0818d418ef46a2b66f946b67a8"
bytes: 7723886
pages: 12
topics: ["perception-3d","mask-r-cnn"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Proposals select continuous regions in a feature map, ROIAlign samples aligned features, and parallel heads predict classes, boxes, and instance masks.","nodes":[{"id":"stage-1","title":"Map regions to features","detail":"Convert image-space proposals into continuous feature-map coordinates.","column":0,"row":0,"section":"Map regions to features","problem_slugs":[],"planned_problems":["Map Proposal Boxes to Feature-Map Coordinates"]},{"id":"stage-2","title":"Sample with ROIAlign","detail":"Use bilinear interpolation at planned points within each pooled bin.","column":1,"row":0,"section":"Sample with ROIAlign","problem_slugs":[],"planned_problems":["Implement bilinear ROI sampling"]},{"id":"stage-3","title":"Predict an instance mask","detail":"Supervise the target class’s mask independently of category competition.","column":2,"row":0,"section":"Predict an instance mask","problem_slugs":[],"planned_problems":["Construct class-specific mask targets","Compare instance-mask IoU and box IoU"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"continuous regions"},{"from":"stage-2","to":"stage-3","label":"aligned region features"}]}
---

## Core paper explanation

Mask R-CNN extends region-based detection with a per-instance mask branch. Its ROIAlign operation preserves spatial correspondence by sampling continuous feature coordinates rather than quantizing region boundaries. Classification, box refinement, and mask prediction share the region features but solve different tasks.

## Execution flow

Proposals select continuous regions in a feature map, ROIAlign samples aligned features, and parallel heads predict classes, boxes, and instance masks.

### Map regions to features

For image-to-feature scale $s$, map $(x,y)$ to $(sx,sy)$ under the implementation’s declared pixel-center convention. A sample at noninteger feature coordinate $(u,v)$ uses neighboring pixels. Retaining those fractional coordinates avoids the boundary rounding of quantized ROI pooling.




**Planned component problem:** Map Proposal Boxes to Feature-Map Coordinates. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Sample with ROIAlign

For feature map $F$ and continuous sample $(u,v)$,

$$
\mathcal B(F,u,v)=\sum_{i,j}F_{ij}
\max(0,1-|u-j|)\max(0,1-|v-i|),
$$

where only the four neighboring integer pixels have nonzero weight. Sample points within each region bin are then aggregated. Coordinate offsets, samples-per-bin, border handling, and reduction mode are contract choices; they must match the expected ROIAlign variant.


**Planned component problems:** Implement bilinear ROI sampling. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Predict an instance mask

For a matched instance of class $c$ and binary target mask $Y$, supervise that class’s mask logits $M_c$ using per-pixel binary cross-entropy:

$$
\mathcal L_{\mathrm{mask}}=-\frac1{HW}\sum_{u,v}
\left[Y_{uv}\log\sigma(M_{c,uv})+(1-Y_{uv})\log(1-\sigma(M_{c,uv}))\right].
$$

This is a sigmoid mask objective for the selected class, not a pixel-wise softmax competing across every category. The total training loss adds classification and box regression. [Box IoU](/problems/box-iou-broadcast) is related localization background; mask IoU must compare pixel sets.


**Planned component problems:** Construct class-specific mask targets; Compare instance-mask IoU and box IoU. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Map Proposal Boxes to Feature-Map Coordinates.
- Implement bilinear ROI sampling.
- Construct class-specific mask targets.
- Compare instance-mask IoU and box IoU.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Instance boundaries matter when a grasp must avoid an adjacent object. Small alignment errors can change a mask around thin handles or contact surfaces. Correct mask interpolation does not establish object identity, depth accuracy, or grasp feasibility.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1703.06870) · [Open-access manuscript](https://arxiv.org/pdf/1703.06870)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
