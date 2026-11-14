---
schema_version: 1
paper_id: "2023-grounding-dino"
title: "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection"
authors: ["Shilong Liu", "Zhaoyang Zeng", "Tianhe Ren", "Feng Li", "Hao Zhang", "Jie Yang", "Qing Jiang", "Chunyuan Li", "Jianwei Yang", "Hang Su", "Jun Zhu", "Lei Zhang"]
year: 2023
venue_or_status: "ECCV 2024"
primary_url: "https://arxiv.org/abs/2303.05499"
pdf_url: "https://arxiv.org/pdf/2303.05499"
local_pdf: "./2023-grounding-dino.pdf"
sha256: "ba1c64ec2ac4fedeb50b269eadc994456a8428dbe64a8dba2673f22df0fa20b3"
bytes: 4329735
pages: 33
topics: ["open-set detection", "phrase grounding", "vision-language fusion", "object detection"]
modalities: ["RGB image", "text prompt"]
track_role: "Language-grounded open-world detection"
open_access_status: "Open-access arXiv manuscript"
redistribution_note: "Retain the original attribution and license metadata; verify source terms before redistributing outside this research workspace."
execution_flow: {"title":"Core execution flow","description":"Encode images and text, select language-relevant queries, then decode boxes and resolve token scores into the requested phrases.","nodes":[{"id":"stage-1","title":"Encode image and text features","detail":"Represent spatial image tokens and valid language tokens for fusion.","column":0,"row":0,"section":"Encode image and text features","problem_slugs":[],"planned_problems":["Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention"]},{"id":"stage-2","title":"Select language-guided queries","detail":"Use compatibility with valid text tokens to prioritize candidate image locations.","column":1,"row":0,"section":"Select language-guided queries","problem_slugs":[],"planned_problems":["Select Language-Guided Object Queries"]},{"id":"stage-3","title":"Resolve boxes to phrases","detail":"Decode spatial predictions and aggregate scores over the requested phrase spans.","column":2,"row":0,"section":"Resolve boxes to phrases","problem_slugs":[],"planned_problems":["Map Text Tokens to Grounded Phrases","Decode Phrase-Labeled Boxes","Build a Grounded Segmentation Pipeline and Trace Failures","Evaluate Localization and Phrase Grounding Separately"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"cross-modal features"},{"from":"stage-2","to":"stage-3","label":"selected queries"}]}
---

## Core paper explanation

Grounding DINO makes object detection conditional on text. It combines image and language features, uses language to help select object queries, and predicts boxes associated with relevant text spans. Unlike a fixed classifier with one permanent category vocabulary, the text input participates in the detection process. Token-to-phrase alignment is therefore part of the output contract.

## Execution flow

Encode images and text, select language-relevant queries, then decode boxes and resolve token scores into the requested phrases.

### Encode image and text features

Let visual features be $V\in\mathbb R^{N\times d}$ and text features $T\in\mathbb R^{L\times d}$. Their compatibility matrix has shape $N\times L$:

$$
S=VT^\top.
$$

Padding and special tokens need explicit masks. [Symmetric CLIP loss](/problems/clip-symmetric-loss) is useful background for image-text compatibility, but Grounding DINO adds spatial and detection-specific processing; it is not just global CLIP retrieval with boxes attached.


**Prerequisite practice:** [Compute Symmetric CLIP Contrastive Loss](/problems/clip-symmetric-loss). These supporting skills do not complete this model stage.


**Planned component problem:** Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Select language-guided queries

A query-ranking abstraction is

$$
r_i=\max_{j:m_j=1}S_{ij},\qquad
\mathcal Q=\operatorname{TopK}_i(r_i).
$$

Here $m_j$ indicates usable text tokens. The paper’s full model includes feature enhancement and a multimodal decoder; this expression isolates the selection concept. Token masks must not let padding win a top-k selection, and tie behavior should be deterministic in a small implementation exercise.


**Planned component problems:** Select Language-Guided Object Queries. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Resolve boxes to phrases

If phrase $g$ occupies token set $J_g$, one explicit teaching aggregation is

$$
s_{ig}=\max_{j\in J_g}\sigma(\ell_{ij}),
$$

where $\ell_{ij}$ is a decoded box-query/token logit. This max rule is an example contract, not a universal phrase-calibration law. Token offsets must map back to the original text span correctly. [Pairwise box IoU](/problems/box-iou-broadcast) supports localization evaluation, while phrase correctness requires its own ground-truth associations.


**Prerequisite practice:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). These supporting skills do not complete this model stage.

**Planned component problems:** Map Text Tokens to Grounded Phrases; Decode Phrase-Labeled Boxes; Build a Grounded Segmentation Pipeline and Trace Failures; Evaluate Localization and Phrase Grounding Separately. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Compute Symmetric CLIP Contrastive Loss](/problems/clip-symmetric-loss). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention.
- Select Language-Guided Object Queries.
- Map Text Tokens to Grounded Phrases.
- Decode Phrase-Labeled Boxes.
- Build a Grounded Segmentation Pipeline and Trace Failures.
- Evaluate Localization and Phrase Grounding Separately.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Language-conditioned detection can identify task-relevant objects from an instruction, but pronouns, spatial relations, and ambiguous noun phrases remain failure modes. A high box/token score is not proof that the detected object is graspable. Preserve text spans and image transforms through the grounding-to-control interface.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2303.05499) · [Open-access manuscript](https://arxiv.org/pdf/2303.05499)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
