---
schema_version: 1
paper_id: "2023-segment-anything"
title: "Segment Anything"
authors: ["Alexander Kirillov", "Eric Mintun", "Nikhila Ravi", "Hanzi Mao", "Chloe Rolland", "Laura Gustafson", "Tete Xiao", "Spencer Whitehead", "Alexander C. Berg", "Wan-Yen Lo", "Piotr Dollar", "Ross Girshick"]
year: 2023
venue_or_status: "ICCV 2023"
primary_url: "https://arxiv.org/abs/2304.02643"
pdf_url: "https://arxiv.org/pdf/2304.02643"
local_pdf: "./2023-segment-anything.pdf"
sha256: "c6ca524e47200c3e542587ca76ac1dbc89cc67340f948c819250d16fdbd90cfb"
bytes: 15644599
pages: 30
topics: ["image segmentation", "promptable models", "foundation models", "data engine"]
modalities: ["RGB image", "point prompts", "box prompts", "mask prompts"]
track_role: "Promptable pixel-level perception"
open_access_status: "Open-access arXiv manuscript"
redistribution_note: "Retain the original attribution and license metadata; verify source terms before redistributing outside this research workspace. The SA-1B dataset has separate access terms and is not included here."
execution_flow: {"title":"Core execution flow","description":"Cache an image embedding, encode the prompt, and decode/rank candidate masks. Reusing an embedding is valid only while the underlying preprocessed image stays unchanged.","nodes":[{"id":"stage-1","title":"Encode and cache the image","detail":"Compute reusable spatial image features with a fixed preprocessing transform.","column":0,"row":0,"section":"Encode and cache the image","problem_slugs":[],"planned_problems":["Reuse Image Embeddings Without Stale-Cache Errors"]},{"id":"stage-2","title":"Encode prompts and ambiguity","detail":"Represent positive/negative points, boxes, or masks for the decoder.","column":1,"row":0,"section":"Encode prompts and ambiguity","problem_slugs":[],"planned_problems":["Encode Positive and Negative Point Prompts","Encode a Box Prompt with Positional Features","Transform Prompt Coordinates Through Image Preprocessing"]},{"id":"stage-3","title":"Rank and filter masks","detail":"Use predicted quality and stability while keeping mask geometry explicit.","column":2,"row":0,"section":"Rank and filter masks","problem_slugs":["sam-mask-ranking","sam-stability-overlap-filter"],"planned_problems":["Build a Grounded Segmentation Pipeline and Trace Failures"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"cached features"},{"from":"stage-2","to":"stage-3","label":"candidate masks"}]}
---

## Core paper explanation

Segment Anything separates expensive image encoding from lightweight prompt-conditioned mask prediction. A single cached image embedding supports repeated point, box, or mask prompts. The decoder can return several plausible masks for an ambiguous prompt and predicts quality scores to rank them. This makes interaction and prompt interpretation central to the system, rather than treating segmentation as one fixed-label classification pass.

## Execution flow

Cache an image embedding, encode the prompt, and decode/rank candidate masks. Reusing an embedding is valid only while the underlying preprocessed image stays unchanged.

### Encode and cache the image

For image $I$, let $F=f_{\mathrm{image}}(I)\in\mathbb R^{h\times w\times d}$. A prompt coordinate $(u,v)$ in original pixels must be mapped through the image resize/pad transform $R$:

$$
\tilde p'=R\,[u,v,1]^\top.
$$

The stored feature grid and prompt coordinates must refer to the same transformed image. Caching by filename alone is unsafe if cropping, resizing, or image contents change.


**Planned component problems:** Reuse Image Embeddings Without Stale-Cache Errors. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Encode prompts and ambiguity

Sparse prompts become token embeddings; dense mask prompts become spatial features. The decoder combines image and prompt information and produces mask-token vectors $w_k$. A compact dynamic-mask interpretation is

$$
M_k(x,y)=w_k^\top F_{\mathrm{up}}(x,y),
$$

where $F_{\mathrm{up}}$ is the upscaled image feature map and $M_k$ is a mask logit. Multiple $k$ values can represent different valid interpretations of one prompt; they should not be averaged into an arbitrary blended object.


**Planned component problems:** Encode Positive and Negative Point Prompts; Encode a Box Prompt with Positional Features; Transform Prompt Coordinates Through Image Preprocessing. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Rank and filter masks

For logit threshold $\theta$ and perturbation $\delta>0$, a threshold-stability measure is

$$
\mathrm{stab}(M)=\frac{|\{M>\theta+\delta\}|}{|\{M>\theta-\delta\}|}.
$$

Define the empty-denominator policy. This measures sensitivity to a small threshold change; it is not ground-truth IoU. A separate learned quality head predicts mask quality. Map masks back through the original image transform before computing object geometry or associating depth pixels.


**Implement this component:** [Rank Candidate Masks with Predicted IoU](/problems/sam-mask-ranking). Each linked exercise implements its stated bounded subcomponent; completing it is not a full-paper reproduction.

**Planned component problems:** Build a Grounded Segmentation Pipeline and Trace Failures. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.


**Runnable component:** [Filter Automatic Masks by Stability and Overlap](/problems/sam-stability-overlap-filter). This uses an explicit binary-mask IoU suppression variant, not the original automatic generator’s box-based NMS.


## Implement the components

- **Runnable component:** [Rank Candidate Masks with Predicted IoU](/problems/sam-mask-ranking). This is a bounded synthetic component, not a complete trained model.

The component below is runnable. Other component ideas remain planned.

**Planned components:**

- Reuse Image Embeddings Without Stale-Cache Errors.
- Encode Positive and Negative Point Prompts.
- Encode a Box Prompt with Positional Features.
- Transform Prompt Coordinates Through Image Preprocessing.
- Build a Grounded Segmentation Pipeline and Trace Failures.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Promptable masks can support interactive labeling and object extraction, but a stable mask can still select the wrong object. Fine boundaries, transparent objects, and unfamiliar sensors may require additional checks. Treat mask quality, semantic identity, and physical affordance as different quantities.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2304.02643) · [Open-access manuscript](https://arxiv.org/pdf/2304.02643)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
