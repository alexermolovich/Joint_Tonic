---
schema_version: 1
paper_id: "2022-owl-vit"
title: "Simple Open-Vocabulary Object Detection with Vision Transformers"
authors: ["Minderer, Matthias","Gritsenko, Alexey","Stone, Austin","Neumann, Maxim","Weissenborn, Dirk","Dosovitskiy, Alexey","Mahendran, Aravindh","Arnab, Anurag","Dehghani, Mostafa","Shen, Zhuoran","Wang, Xiao","Zhai, Xiaohua","Kipf, Thomas","Houlsby, Neil"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2205.06230"
pdf_url: "https://arxiv.org/pdf/2205.06230"
local_pdf: "./2022-owl-vit.pdf"
sha256: "3d38f1ae5c64a45203c51e3dda842dfc866228e744952d52547de55f284cd23d"
bytes: 4116627
pages: 28
topics: ["vlm-grounding","owl-vit"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Keep spatial tokens","detail":"Replace global pooling with token-level detection heads.","column":0,"row":0,"section":"Keep spatial tokens","problem_slugs":[],"planned_problems":["Attach Text-Scoring and Box Heads to Spatial Vision Tokens"]},{"id":"stage-2","title":"Score query regions","detail":"Use text embeddings as dynamic class representations.","column":1,"row":0,"section":"Score query regions","problem_slugs":[],"planned_problems":["Build Text-Conditioned Detection Scores","Select Boxes for a Query Phrase"]},{"id":"stage-3","title":"Train matched boxes","detail":"Match object targets to predictions without duplicate assignments.","column":2,"row":0,"section":"Train matched boxes","problem_slugs":[],"planned_problems":["Evaluate Seen and Unseen Class Slices"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"region embeddings"},{"from":"stage-2","to":"stage-3","label":"scores and boxes"}]}
---

## Core paper explanation

OWL-ViT transfers a contrastively pretrained image–text model to open-vocabulary detection. Removing image pooling exposes per-token features; lightweight heads predict boxes and compare region embeddings with text or image-derived queries.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Keep spatial tokens

For $N$ image tokens, the vision transformer produces $H\in\mathbb R^{N\times d}$. Heads produce boxes $B\in\mathbb R^{N\times4}$ and query-comparable embeddings $E\in\mathbb R^{N\times d_e}$. Spatial tokens retain candidate locations that global image pooling would discard.




**Planned component problem:** Attach Text-Scoring and Box Heads to Spatial Vision Tokens. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Score query regions

For $C$ query embeddings $T\in\mathbb R^{C\times d_e}$, normalized similarity is
$$s_{ic}=\frac{e_i^\top t_c}{\|e_i\|_2\|t_c\|_2}.$$
The detection classifier includes learned scoring calibration. Text and image-query embeddings can share the query interface because the encoders are not fused per query.


**Planned component problems:** Build Text-Conditioned Detection Scores; Select Boxes for a Query Phrase. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Train matched boxes

Detection fine-tuning uses bipartite matching:
$$\pi^*=\arg\min_\pi\sum_j C(\hat b_{\pi(j)},\hat s_{\pi(j)},b_j,c_j).$$
$\pi$ assigns each annotated object to a distinct prediction; cost includes class and box terms. Unmatched predictions receive background supervision. Training updates both image and text models.


**Prerequisite practice:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). These supporting skills do not complete this model stage.

**Planned component problems:** Evaluate Seen and Unseen Class Slices. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Compute Symmetric CLIP Contrastive Loss](/problems/clip-symmetric-loss). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Attach Text-Scoring and Box Heads to Spatial Vision Tokens.
- Build Text-Conditioned Detection Scores.
- Select Boxes for a Query Phrase.
- Evaluate Seen and Unseen Class Slices.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

An instruction can name an object not in a fixed training label list. Query wording, small objects, and visually similar distractors still matter; evaluate box localization separately from successful grasping.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2205.06230) · [Open-access manuscript](https://arxiv.org/pdf/2205.06230)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
