---
schema_version: 1
paper_id: "2025-smolvla"
title: "SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics"
authors: ["Shukor, Mustafa","Aubakirova, Dana","Capuano, Francesco","Kooijmans, Pepijn","Palma, Steven","Zouitine, Adil","Aractingi, Michel","Pascal, Caroline","Russi, Martino","Marafioti, Andres","Alibert, Simon","Cord, Matthieu","Wolf, Thomas","Cadene, Remi"]
year: 2025
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2506.01844"
pdf_url: "https://arxiv.org/pdf/2506.01844"
local_pdf: "./2025-smolvla.pdf"
sha256: "cb1bb9a8f824187fcdc32af8c290214487c524f139a3c2def1c6d97adb1fa40c"
bytes: 8921356
pages: 24
topics: ["vla-generalist","smolvla"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Encode visual and state context","detail":"Use a compact VLM and alternating action-expert attention.","column":0,"row":0,"section":"Encode visual and state context","problem_slugs":[],"planned_problems":["Normalize a Compact VLA Observation Batch"]},{"id":"stage-2","title":"Learn an action flow","detail":"Map Gaussian chunks toward demonstrated actions.","column":1,"row":0,"section":"Learn an action flow","problem_slugs":[],"planned_problems":["Construct a Compact Policy Flow-Matching Target"]},{"id":"stage-3","title":"Refill the action queue","detail":"Predict asynchronously before the current chunk is exhausted.","column":2,"row":0,"section":"Refill the action queue","problem_slugs":["edge-inference-release-gate"],"planned_problems":["Schedule Asynchronous Policy Chunks","Measure Stale-Action Latency"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"context features"},{"from":"stage-2","to":"stage-3","label":"generated chunk"}]}
---
## Core paper explanation

SmolVLA pairs a compact vision-language backbone with a flow-matching action expert and asynchronous inference. Its deployment design separates action execution from generating the next action chunk, reducing idle control time when predictions take multiple control ticks.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Encode visual and state context

Context $c$ contains image, instruction, and robot-state information. The action expert alternates self-attention over noisy action representations with cross-attention to VLM features. Its output has chunk shape $H\times d$, where $H$ is the action horizon and $d$ the embodiment's action dimension.

<!-- joint-tonic-component:stage-1 -->
- **Planned component:** Normalize a Compact VLA Observation Batch. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Learn an action flow

For the noise-to-data convention $A_\tau=(1-\tau)E+\tau A$,
$$L=\mathbb E\|v_\theta(A_\tau,\tau,c)-(A-E)\|_F^2.$$
Inference integrates the learned vector field from noise to action. This is flow matching, not the DDPM noise-prediction target. Match the released model's interpolation direction and numerical integration setup.

<!-- joint-tonic-component:stage-2 -->
- **Planned component:** Construct a Compact Policy Flow-Matching Target. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Refill the action queue

The paper's queue trigger compares remaining actions $n_{\mathrm{remain}}$ with chunk size $H$:
$$n_{\mathrm{remain}}/H<g,\qquad g\in[0,1].$$
A new observation can trigger a nonblocking prediction; overlap aggregation merges compatible pending/new actions. Timestamp each chunk so delayed results cannot silently overwrite more recent control intent.

<!-- joint-tonic-component:stage-3 -->
- **Related implementation prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).
- **Planned component:** Schedule Asynchronous Policy Chunks. This is an idea or blueprint, not a runnable exercise yet.
- **Planned component:** Measure Stale-Action Latency. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

## Implement the components

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate)

Planned components: Normalize a Compact VLA Observation Batch; Construct a Compact Policy Flow-Matching Target; Schedule Asynchronous Policy Chunks; Measure Stale-Action Latency. Exact approved curriculum titles are reused where available; additional named ideas require a reviewed blueprint before implementation.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Asynchronous execution can improve responsiveness on modest hardware. Queue underruns, stale predictions, and abrupt overlap transitions are distinct failure modes; measure observation age and action continuity, not only model inference time.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2506.01844) · [Open-access manuscript](https://arxiv.org/pdf/2506.01844)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
