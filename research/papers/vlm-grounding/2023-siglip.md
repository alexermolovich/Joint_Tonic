---
schema_version: 1
paper_id: "2023-siglip"
title: "Sigmoid Loss for Language Image Pre-Training"
authors: ["Zhai, Xiaohua","Mustafa, Basil","Kolesnikov, Alexander","Beyer, Lucas"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2303.15343"
pdf_url: "https://arxiv.org/pdf/2303.15343"
local_pdf: "./2023-siglip.pdf"
sha256: "2efade8de3baeffe9eba759aab9f510ea8f8ac3c365f02f0da75d9baf9ffa2db"
bytes: 614960
pages: 17
topics: ["vlm-grounding","siglip"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Construct pair labels","detail":"Mark matched pairs positive and other pairs negative.","column":0,"row":0,"section":"Construct pair labels","problem_slugs":[],"planned_problems":["Build Positive-Negative Pair Masks"]},{"id":"stage-2","title":"Compute sigmoid loss","detail":"Accumulate stable binary pair losses.","column":1,"row":0,"section":"Compute sigmoid loss","problem_slugs":[],"planned_problems":["Compute Pairwise Sigmoid Alignment Loss"]},{"id":"stage-3","title":"Chunk pair computation","detail":"Accumulate pair blocks without softmax normalization.","column":2,"row":0,"section":"Chunk pair computation","problem_slugs":[],"planned_problems":["Compare Batch-Size Sensitivity"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"pair logits"},{"from":"stage-2","to":"stage-3","label":"pairwise losses"}]}
---

## Core paper explanation

SigLIP replaces batch-normalized contrastive softmax with independent binary image–text pair classification. It can process pair blocks without needing a global softmax denominator, while retaining normalized image/text embeddings.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Construct pair labels

For $B$ paired examples, set $z_{ij}=1$ when $i=j$ and $z_{ij}=-1$ otherwise. Normalized embeddings $v_i,t_j\in\mathbb R^d$ yield
$$s_{ij}=e^a v_i^\top t_j+b,$$
with learned log-scale $a$ and bias $b$. The bias addresses the large imbalance between positive and negative pairs.


**Planned component problems:** Build Positive-Negative Pair Masks. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Compute sigmoid loss

Using the paper's per-example normalization,
$$L=\frac1B\sum_{i=1}^B\sum_{j=1}^B\log(1+e^{-z_{ij}s_{ij}}).$$
Implement this with a stable softplus/log-sigmoid operation. Dividing by $B^2$ instead changes gradient scale; document any teaching deviation. This is not the symmetric softmax objective in the CLIP exercise.


**Planned component problems:** Compute Pairwise Sigmoid Alignment Loss. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Chunk pair computation

For disjoint pair blocks $\mathcal P_k$ covering all desired pairs,
$$L=\frac1B\sum_k\sum_{(i,j)\in\mathcal P_k}\operatorname{softplus}(-z_{ij}s_{ij}).$$
This decomposition preserves the full loss when all pairs are included. Sampling negatives changes the objective unless weighting accounts for the sampling scheme.


**Planned component problems:** Compare Batch-Size Sensitivity. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Compute Symmetric CLIP Contrastive Loss](/problems/clip-symmetric-loss). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Build Positive-Negative Pair Masks.
- Compute Pairwise Sigmoid Alignment Loss.
- Compare Batch-Size Sensitivity.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

The pairwise objective can support large robot image–language datasets with limited memory. Duplicate instructions and visually equivalent scenes create false negatives; data identity and semantic overlap remain important even with a different loss.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2303.15343) · [Open-access manuscript](https://arxiv.org/pdf/2303.15343)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
