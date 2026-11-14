---
schema_version: 1
paper_id: "2023-llava"
title: "Visual Instruction Tuning"
authors: ["Liu, Haotian","Li, Chunyuan","Wu, Qingyang","Lee, Yong Jae"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2304.08485"
pdf_url: "https://arxiv.org/pdf/2304.08485"
local_pdf: "./2023-llava.pdf"
sha256: "dc8bace378a282ea78caa9b5959306202fbfa3b8cedaf8a66541a9af18f4d3bf"
bytes: 5906135
pages: 25
topics: ["vlm-grounding","llava"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Project visual tokens","detail":"Align vision features to the language embedding width.","column":0,"row":0,"section":"Project visual tokens","problem_slugs":[],"planned_problems":["Project Visual Tokens into Language Width"]},{"id":"stage-2","title":"Format conversations","detail":"Mark human context and assistant targets.","column":1,"row":0,"section":"Format conversations","problem_slugs":[],"planned_problems":["Mask Visual-Instruction Training Labels","Collate Variable Image-Text Conversations"]},{"id":"stage-3","title":"Tune and answer","detail":"Update the projection and language model on instructions.","column":2,"row":0,"section":"Tune and answer","problem_slugs":[],"planned_problems":["Compute an Assistant-Only Visual-Instruction Loss"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"visual embeddings"},{"from":"stage-2","to":"stage-3","label":"masked targets"}]}
---

## Core paper explanation

The original LLaVA connects a CLIP visual encoder to a language model through a learned projection, then trains on visual instruction-following conversations. Its key learning interface is assistant-response prediction conditioned on image features and conversation history.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Project visual tokens

With visual features $Z_v\in\mathbb R^{N\times d_v}$, the original paper uses a linear projection:
$$H_v=Z_vW,\qquad W\in\mathbb R^{d_v\times d_{\mathrm{LM}}}.$$
Later LLaVA variants use other projectors; this card describes the original paper. Feature alignment first trains the projection with the pretrained backbones frozen.


**Planned component problems:** Project Visual Tokens into Language Width. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Format conversations

A conversation contains system/context tokens, user instructions, assistant answers, and separators. Let $m_t=1$ only for supervised assistant answer and stop tokens. The objective is
$$L=-\frac{\sum_t m_t\log p_\theta(y_t\mid y_{<t},H_v)}{\sum_t m_t}.$$
Masking prevents training the model to regenerate user prompts as if they were answers. Reject examples with no supervised tokens.


**Planned component problems:** Mask Visual-Instruction Training Labels; Collate Variable Image-Text Conversations. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Tune and answer

Instruction tuning updates the language model and projection while retaining the visual encoder. At inference, autoregressive generation uses image features plus prior turns; no reference answer is supplied. Evaluate whether claims are supported by the image, not just whether the response is grammatical.




**Planned component problem:** Compute an Assistant-Only Visual-Instruction Loss. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

## Implement the components

The stage-specific implementation ideas above are not runnable yet. A reviewed blueprint and evaluator are required before publication.

**Planned components:**

- Project Visual Tokens into Language Width.
- Mask Visual-Instruction Training Labels.
- Collate Variable Image-Text Conversations.
- Compute an Assistant-Only Visual-Instruction Loss.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

A visual assistant can explain observations or help inspect a robot dataset. It is not a motor controller, and hallucinated objects or spatial relations should never be silently converted into physical commands.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2304.08485) · [Open-access manuscript](https://arxiv.org/pdf/2304.08485)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
