---
schema_version: 1
paper_id: "2021-align"
title: "Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision"
authors: ["Jia, Chao","Yang, Yinfei","Xia, Ye","Chen, Yi-Ting","Parekh, Zarana","Pham, Hieu","Le, Quoc V.","Sung, Yunhsuan","Li, Zhen","Duerig, Tom"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2102.05918"
pdf_url: "https://arxiv.org/pdf/2102.05918"
local_pdf: "./2021-align.pdf"
sha256: "dd9e1884b4593af667a176dcaabc0399effd1b278130804660ec8f6ae82fcfc4"
bytes: 2038832
pages: 14
topics: ["vlm-grounding","align"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Encode paired data","detail":"Normalize image and text embeddings.","column":0,"row":0,"section":"Encode paired data","problem_slugs":["clip-normalize-embeddings"],"planned_problems":["Deduplicate Image-Text Training Pairs"]},{"id":"stage-2","title":"Train alignment","detail":"Classify the matching partner in both directions.","column":1,"row":0,"section":"Train alignment","problem_slugs":["clip-symmetric-loss"],"planned_problems":["Construct Contrastive Pair Labels"]},{"id":"stage-3","title":"Retrieve or classify","detail":"Compare one embedding against a candidate bank.","column":2,"row":0,"section":"Retrieve or classify","problem_slugs":["clip-retrieval-recall"],"planned_problems":["Compute Retrieval Recall by Slice"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"paired embeddings"},{"from":"stage-2","to":"stage-3","label":"trained encoders"}]}
---

## Core paper explanation

ALIGN learns a shared image–text space from a large, noisy collection of paired images and captions. Its central choice is a simple dual encoder: retrieval needs one embedding per item rather than cross-attention for every candidate pair.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Encode paired data

For a batch of $B$ paired images and captions, the encoders produce unit vectors $v_i,t_i\in\mathbb R^d$. Similarity is dimensionless:
$$s_{ij}=v_i^\top t_j/\tau,\qquad \|v_i\|_2=\|t_i\|_2=1,$$
where $\tau>0$ is the learned temperature. Pair identity must survive shuffling and distributed gathering.


**Implement this component:** [Normalize Image and Text Embeddings](/problems/clip-normalize-embeddings). The reusable normalization component requires equal-sized paired batches; it does not build encoders.

**Planned component problems:** Deduplicate Image-Text Training Pairs. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Train alignment

Each row treats its paired caption as positive; each column treats its paired image as positive:
$$L=-\frac1{2B}\sum_i\left[\log\frac{e^{s_{ii}}}{\sum_j e^{s_{ij}}}+\log\frac{e^{s_{ii}}}{\sum_j e^{s_{ji}}}\right].$$
This is the same symmetric contrastive mechanism practiced in the linked CLIP exercise. Other captions in the batch can be false negatives; data scale does not make that assumption exact.


**Implement this component:** [Compute Symmetric CLIP Contrastive Loss](/problems/clip-symmetric-loss). The symmetric loss is a reusable paired-batch contrastive component. Large-scale ALIGN training and data cleaning remain outside its contract.

**Planned component problems:** Construct Contrastive Pair Labels. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Retrieve or classify

For candidate descriptions $c$, choose $\hat c=\arg\max_c v^\top t_c$. The score ranks candidates; it is not a calibrated probability that a robot can grasp the object. Cache embeddings only with the encoder and preprocessing versions that produced them.


**Implement this component:** [Evaluate Cross-Modal Retrieval Recall at K](/problems/clip-retrieval-recall). The retrieval evaluator assumes one diagonal positive per query and defines deterministic tie handling; richer relevance sets need a different evaluator.

**Planned component problems:** Compute Retrieval Recall by Slice. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Compute Symmetric CLIP Contrastive Loss](/problems/clip-symmetric-loss). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Deduplicate Image-Text Training Pairs.
- Construct Contrastive Pair Labels.
- Compute Retrieval Recall by Slice.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Language retrieval can select relevant robot images or observations. Similar appearance and noisy captions can merge distinct objects; evaluate on unseen scenes and instruction paraphrases, not only near-duplicate images.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2102.05918) · [Open-access manuscript](https://arxiv.org/pdf/2102.05918)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
