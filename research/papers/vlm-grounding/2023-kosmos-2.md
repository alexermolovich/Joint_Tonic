---
schema_version: 1
paper_id: "2023-kosmos-2"
title: "Kosmos-2: Grounding Multimodal Large Language Models to the World"
authors: ["Peng, Zhiliang","Wang, Wenhui","Dong, Li","Hao, Yaru","Huang, Shaohan","Ma, Shuming","Wei, Furu"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2306.14824"
pdf_url: "https://arxiv.org/pdf/2306.14824"
local_pdf: "./2023-kosmos-2.pdf"
sha256: "064214db82bb573831fd102ace00be90147633e7f47dac491089619e03bc7e58"
bytes: 7580509
pages: 20
topics: ["vlm-grounding","kosmos-2"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Encode locations","detail":"Map two-dimensional positions to location tokens.","column":0,"row":0,"section":"Encode locations","problem_slugs":[],"planned_problems":["Encode Grounding Locations as Tokens"]},{"id":"stage-2","title":"Link phrases and boxes","detail":"Keep text spans attached to their spatial references.","column":1,"row":0,"section":"Link phrases and boxes","problem_slugs":[],"planned_problems":["Map Text Spans to Image Boxes"]},{"id":"stage-3","title":"Learn grounded sequences","detail":"Predict both ordinary and location tokens.","column":2,"row":0,"section":"Learn grounded sequences","problem_slugs":[],"planned_problems":["Validate Grounded Sequence Syntax"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"location tokens"},{"from":"stage-2","to":"stage-3","label":"grounded sequences"}]}
---

## Core paper explanation

KOSMOS-2 associates text spans with image regions by adding location tokens to multimodal language modeling. The model can both interpret a referenced region and generate grounded text whose phrases point to bounding boxes.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Encode locations

The paper divides image width and height into $32$ bins, giving $32\times32$ location tokens. A row-major teaching convention is
$$q=q_y\,32+q_x,\qquad q_x,q_y\in\{0,\ldots,31\}.$$
Use the tokenizer's actual index convention when interoperating with weights. Two corner positions describe a box; these are image coordinates, not world-frame positions.


**Planned component problems:** Encode Grounding Locations as Tokens. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Link phrases and boxes

For phrase tokens $w_{a:b}$, a structured output groups that span with its box location tokens. A basic validity condition is
$$0\le x_1\le x_2\le1,\qquad 0\le y_1\le y_2\le1.$$
This is a geometry check for decoded normalized corners, not the language-model objective. Preserve separators and support phrases referring to multiple boxes.


**Planned component problems:** Map Text Spans to Image Boxes. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Learn grounded sequences

Training applies next-token likelihood to discrete text and location tokens:
$$L=-\sum_{t\in\mathcal D}\log p_\theta(y_t\mid y_{<t},I),$$
where $\mathcal D$ indexes supervised discrete tokens. Visual feature positions are conditioning inputs, not discrete targets. Grounded image–text data supplies the phrase/region associations.


**Planned component problems:** Validate Grounded Sequence Syntax. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Encode Grounding Locations as Tokens.
- Map Text Spans to Image Boxes.
- Validate Grounded Sequence Syntax.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Grounded language can make “pick this object” more explicit. The finite location grid limits precision, and a fluent phrase can still reference the wrong box; keep grounding evaluation separate from language quality.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2306.14824) · [Open-access manuscript](https://arxiv.org/pdf/2306.14824)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
