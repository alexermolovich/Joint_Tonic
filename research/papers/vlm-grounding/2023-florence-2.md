---
schema_version: 1
paper_id: "2023-florence-2"
title: "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks"
authors: ["Xiao, Bin","Wu, Haiping","Xu, Weijian","Dai, Xiyang","Hu, Houdong","Lu, Yumao","Zeng, Michael","Liu, Ce","Yuan, Lu"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2311.06242"
pdf_url: "https://arxiv.org/pdf/2311.06242"
local_pdf: "./2023-florence-2.pdf"
sha256: "403d820e5ea7a1d7e2f95d4b2facef3ea37e2a5f12354a8a50164b10a057708a"
bytes: 56176792
pages: 35
topics: ["vlm-grounding","florence-2"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Encode task and image","detail":"Combine visual evidence with the requested task.","column":0,"row":0,"section":"Encode task and image","problem_slugs":[],"planned_problems":["Route Task Prompts to Output Schemas"]},{"id":"stage-2","title":"Generate spatial tokens","detail":"Represent coordinates inside the output vocabulary.","column":1,"row":0,"section":"Generate spatial tokens","problem_slugs":[],"planned_problems":["Normalize Spatial Coordinates into Tokens"]},{"id":"stage-3","title":"Train and parse outputs","detail":"Apply token loss, then validate the task grammar.","column":2,"row":0,"section":"Train and parse outputs","problem_slugs":[],"planned_problems":["Parse Structured Detection Tokens"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"multimodal context"},{"from":"stage-2","to":"stage-3","label":"text and location tokens"}]}
---

## Core paper explanation

Florence-2 represents diverse vision tasks as prompted sequence generation. Its vocabulary contains location tokens, allowing one encoder–decoder to describe images and produce structured boxes, OCR quadrilaterals, or polygons.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Encode task and image

A DaViT visual encoder and text task prompt form conditioning input $x$. The sequence model learns
$$p(y\mid x)=\prod_{t=1}^{|y|}p(y_t\mid y_{<t},x).$$
A task prompt determines the output grammar; it is not merely an extra descriptive caption.


**Planned component problems:** Route Task Prompts to Output Schemas. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Generate spatial tokens

For a normalized coordinate $u\in[0,1]$, a pedagogical $Q$-bin codec is
$$q=\min(Q-1,\lfloor Qu\rfloor),\qquad \hat u=(q+1/2)/Q.$$
This illustrates quantization; an implementation must use the released tokenizer's precise rounding and dequantization rules. Florence-2 emits box corners, ordered OCR quadrilaterals, or polygon vertices according to the task.


**Planned component problems:** Normalize Spatial Coordinates into Tokens. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Train and parse outputs

Training uses
$$L=-\sum_t\log p_\theta(y_t\mid y_{<t},x).$$
At inference, parse the generated sequence into typed objects, reject incomplete coordinate groups, and map coordinates through the image preprocessing transform. Evaluate geometry with task metrics rather than token accuracy alone.


**Prerequisite practice:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). These supporting skills do not complete this model stage.

**Planned component problems:** Parse Structured Detection Tokens. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Route Task Prompts to Output Schemas.
- Normalize Spatial Coordinates into Tokens.
- Parse Structured Detection Tokens.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Structured generation can populate an object inventory from a camera frame. Quantization, invalid geometry, and incorrect rescaling can move a grasp target; box predictions are not metric 3D coordinates.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2311.06242) · [Open-access manuscript](https://arxiv.org/pdf/2311.06242)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
