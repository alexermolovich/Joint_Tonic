---
schema_version: 1
paper_id: "2022-flamingo"
title: "Flamingo: a Visual Language Model for Few-Shot Learning"
authors: ["Alayrac, Jean-Baptiste","Donahue, Jeff","Luc, Pauline","Miech, Antoine","Barr, Iain","Hasson, Yana","Lenc, Karel","Mensch, Arthur","Millican, Katie","Reynolds, Malcolm","Ring, Roman","Rutherford, Eliza","Cabi, Serkan","Han, Tengda","Gong, Zhitao","Samangooei, Sina","Monteiro, Marianne","Menick, Jacob","Borgeaud, Sebastian","Brock, Andrew","Nematzadeh, Aida","Sharifzadeh, Sahand","Binkowski, Mikolaj","Barreira, Ricardo","Vinyals, Oriol","Zisserman, Andrew","Simonyan, Karen"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2204.14198"
pdf_url: "https://arxiv.org/pdf/2204.14198"
local_pdf: "./2022-flamingo.pdf"
sha256: "27af622bf50987fd98a03451a27a670adfaeefd5218a3e990b37abc326ba63f0"
bytes: 31579390
pages: 54
topics: ["vlm-grounding","flamingo"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Resample visual features","detail":"Compress variable-sized features into a fixed token set.","column":0,"row":0,"section":"Resample visual features","problem_slugs":[],"planned_problems":["Resample Variable Visual Features"]},{"id":"stage-2","title":"Gate visual conditioning","detail":"Inject image information into language layers.","column":1,"row":0,"section":"Gate visual conditioning","problem_slugs":[],"planned_problems":["Gate a Multimodal Residual Update"]},{"id":"stage-3","title":"Predict interleaved text","detail":"Train next-token prediction; prompt at inference.","column":2,"row":0,"section":"Predict interleaved text","problem_slugs":[],"planned_problems":["Mask Cross-Attention by Image Position"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"visual tokens"},{"from":"stage-2","to":"stage-3","label":"conditioned language state"}]}
---

## Core paper explanation

Flamingo connects a frozen visual encoder and frozen language model with trainable visual resampling and gated cross-attention. It accepts interleaved images and text, enabling few-shot prompting without updating the large pretrained backbones.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Resample visual features

The image encoder yields $X\in\mathbb R^{N\times d_v}$. Learned latent queries $Q\in\mathbb R^{M\times d}$ produce a fixed-length visual representation. The cross-attention mechanism is
$$Z=\operatorname{softmax}(QK^\top/\sqrt d)V,$$
where keys and values incorporate visual features; the actual Perceiver Resampler also allows latent information into its attention. $M$ stays fixed as image/video feature count changes.


**Planned component problems:** Resample Variable Visual Features. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Gate visual conditioning

A simplified gated residual is
$$h'=h+\tanh(\alpha)\operatorname{CrossAttn}(h,Z).$$
The learned scalar gate starts at zero, preserving the pretrained language computation initially. Gated dense layers accompany the attention layers. Image-causal masking controls which visual input each text position can attend to.


**Planned component problems:** Gate a Multimodal Residual Update. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Predict interleaved text

For text sequence $y$, the likelihood is
$$p(y\mid X)=\prod_t p(y_t\mid y_{<t},X_{\le t}).$$
$X_{\le t}$ denotes visual inputs preceding position $t$. The implementation's direct cross-attention mask selects the most recent preceding image; language self-attention can carry earlier context. Demonstrations in a prompt are context, not gradient updates.


**Planned component problems:** Mask Cross-Attention by Image Position. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

The stage-specific implementation ideas above are not runnable yet. A reviewed blueprint and evaluator are required before publication.

**Planned components:**

- Resample Variable Visual Features.
- Gate a Multimodal Residual Update.
- Mask Cross-Attention by Image Position.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Visual-language context can explain a scene history, but generated descriptions do not provide calibrated contact state or control guarantees. Long histories, stale frames, and incorrect image/text ordering can change an answer.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2204.14198) · [Open-access manuscript](https://arxiv.org/pdf/2204.14198)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
