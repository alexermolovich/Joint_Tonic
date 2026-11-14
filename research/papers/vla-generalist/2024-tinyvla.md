---
schema_version: 1
paper_id: "2024-tinyvla"
title: "TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation"
authors: ["Wen, Junjie","Zhu, Yichen","Li, Jinming","Zhu, Minjie","Wu, Kun","Xu, Zhiyuan","Liu, Ning","Cheng, Ran","Shen, Chaomin","Peng, Yaxin","Feng, Feifei","Tang, Jian"]
year: 2024
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2409.12514"
pdf_url: "https://arxiv.org/pdf/2409.12514"
local_pdf: "./2024-tinyvla.pdf"
sha256: "57a8d723e8ec76f8c6fee0e74944b8f7308b87cabe6bd327050ae9ebb4a9753f"
bytes: 4781062
pages: 8
topics: ["vla-generalist","tinyvla"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Build compact conditioning","detail":"Pool multimodal features and combine proprioception.","column":0,"row":0,"section":"Build compact conditioning","problem_slugs":[],"planned_problems":["Project Compact Visual-Language Features"]},{"id":"stage-2","title":"Train action denoising","detail":"Predict the noise added to demonstration chunks.","column":1,"row":0,"section":"Train action denoising","problem_slugs":["diffusion-action-noising"],"planned_problems":["Build a Small Action Decoder"]},{"id":"stage-3","title":"Sample continuous actions","detail":"Iteratively denoise, restore physical units, and execute a prefix.","column":2,"row":0,"section":"Sample continuous actions","problem_slugs":[],"planned_problems":["Estimate End-to-End Policy Memory"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"conditioning vector"},{"from":"stage-2","to":"stage-3","label":"trained denoiser"}]}
---
## Core paper explanation

TinyVLA combines a compact pretrained vision-language backbone with a diffusion policy decoder. It focuses on efficient adaptation from relatively small robot datasets while retaining continuous, multimodal action prediction.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Build compact conditioning

The VLM produces variable-length features $H$. Adaptive pooling and normalization create a fixed representation, then a multilayer perceptron combines it with robot state $q$:
$$c=\operatorname{MLP}([\operatorname{LN}(\operatorname{Pool}(H));q]).$$
The state vector must retain joint ordering, units, and normalization metadata.

<!-- joint-tonic-component:stage-1 -->
- **Planned component:** Project Compact Visual-Language Features. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Train action denoising

For normalized chunk $A^0\in\mathbb R^{H_a\times d_a}$ and Gaussian noise $\epsilon$,
$$A^k=\sqrt{\bar\alpha_k}A^0+\sqrt{1-\bar\alpha_k}\epsilon,\qquad L=\mathbb E\|\epsilon-\epsilon_\theta(A^k,k,c)\|_2^2.$$
$\bar\alpha_k$ is the cumulative diffusion schedule. The linked exercise implements the forward-noising tensor contract, not TinyVLA's trained decoder.

<!-- joint-tonic-component:stage-2 -->
- **Related implementation prerequisite:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising).
- **Planned component:** Build a Small Action Decoder. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Sample continuous actions

Inference starts from noise and applies the configured reverse diffusion updates. Generated normalized actions must be transformed back into the embodiment's units before execution. End-to-end latency includes images, feature encoding, all denoising steps, and the controller interface.

<!-- joint-tonic-component:stage-3 -->
- **Planned component:** Estimate End-to-End Policy Memory. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

## Implement the components

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Add Noise to an Action Sequence](/problems/diffusion-action-noising)

Planned components: Project Compact Visual-Language Features; Build a Small Action Decoder; Estimate End-to-End Policy Memory. Exact approved curriculum titles are reused where available; additional named ideas require a reviewed blueprint before implementation.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Compact models can fit tighter robot compute budgets. Lower parameter count alone does not guarantee lower control delay, and action normalization errors can overwhelm improvements in visual understanding.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2409.12514) · [Open-access manuscript](https://arxiv.org/pdf/2409.12514)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
