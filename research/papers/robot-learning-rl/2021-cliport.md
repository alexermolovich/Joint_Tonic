---
schema_version: 1
paper_id: "2021-cliport"
title: "CLIPort: What and Where Pathways for Robotic Manipulation"
authors: ["Shridhar, Mohit","Manuelli, Lucas","Fox, Dieter"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2109.12098"
pdf_url: "https://arxiv.org/pdf/2109.12098"
local_pdf: "./2021-cliport.pdf"
sha256: "3cc19664beabda203cb1a1ad86659f75f60a099189820d92d59d20067c9ab003"
bytes: 8143919
pages: 24
topics: ["robot-learning-rl","cliport"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Encode semantic instructions","detail":"Use pretrained CLIP representations for visual-language meaning.","column":0,"row":0,"section":"Encode semantic instructions","problem_slugs":[],"planned_problems":["Align Instruction Embeddings with Manipulation Observations"]},{"id":"stage-2","title":"Fuse spatial and semantic streams","detail":"Combine language-aware features with precise scene geometry.","column":1,"row":0,"section":"Fuse spatial and semantic streams","problem_slugs":[],"planned_problems":["Fuse Semantic and Spatial Feature Streams","Condition a Place Map on a Language Goal"]},{"id":"stage-3","title":"Imitate language-conditioned actions","detail":"Train pick and placement classification from demonstrations.","column":2,"row":0,"section":"Imitate language-conditioned actions","problem_slugs":[],"planned_problems":["Compute Language-Conditioned Pick-and-Place Cross-Entropy","Evaluate Compositional Manipulation Slices"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"semantic features"},{"from":"stage-2","to":"stage-3","label":"fused action maps"}]}
---

## Core paper explanation

CLIPort combines pretrained vision-language semantics with the spatial action structure of Transporter Networks. One pathway supplies what an instruction refers to, while another preserves the spatial detail needed for precise manipulation.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Encode semantic instructions

Language embedding $l=E_{\mathrm{text}}(\ell)$ conditions semantic visual features. These pretrained embeddings are not sufficient by themselves to specify a metric grasp pose. The paper uses CLIP representations rather than retraining CLIP's contrastive loss as its main robot objective.


**Planned exercise:** Align Instruction Embeddings with Manipulation Observations.


### Fuse spatial and semantic streams

Denote the fused pick map by $p(u\mid o,\ell)$ and place map by $p(v\mid o,\ell,u)$. Transporter-style cross-correlation carries a selected pick feature to candidate placements, while the instruction disambiguates desired objects and relations.


**Planned exercise:** Fuse Semantic and Spatial Feature Streams.

**Planned exercise:** Condition a Place Map on a Language Goal.


### Imitate language-conditioned actions

The action loss is
$$L=-\log p(u^*\mid o,\ell)-\log p(v^*\mid o,\ell,u^*).$$
Rotation bins and robot execution conventions must be retained. Evaluate compositional language and object variation separately from familiar task repetition.


**Planned exercise:** Compute Language-Conditioned Pick-and-Place Cross-Entropy.

**Planned exercise:** Evaluate Compositional Manipulation Slices.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Encode semantic instructions:** Align Instruction Embeddings with Manipulation Observations (planned).
- **Fuse spatial and semantic streams:** Fuse Semantic and Spatial Feature Streams (planned); Condition a Place Map on a Language Goal (planned).
- **Imitate language-conditioned actions:** Compute Language-Conditioned Pick-and-Place Cross-Entropy (planned); Evaluate Compositional Manipulation Slices (planned).

## Why this matters on a robot

Semantic priors help interpret instructions such as placing a named object in a specified region. Precise manipulation still depends on geometry, calibration, and controller feasibility; language similarity is not an action-success score.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2109.12098) · [Open-access manuscript](https://arxiv.org/pdf/2109.12098)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
