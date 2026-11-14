---
schema_version: 1
paper_id: "2025-openvla-oft"
title: "Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success"
authors: ["Kim, Moo Jin","Finn, Chelsea","Liang, Percy"]
year: 2025
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2502.19645"
pdf_url: "https://arxiv.org/pdf/2502.19645"
local_pdf: "./2025-openvla-oft.pdf"
sha256: "b860aa1206b6cfb0ce8be177f961379dd6a133d52cc74ac346636e0f4952a596"
bytes: 26994977
pages: 24
topics: ["vla-generalist","openvla-oft"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Encode context and action slots","detail":"Condition a chunk of output positions on the current observation.","column":0,"row":0,"section":"Encode context and action slots","problem_slugs":[],"planned_problems":["Construct Parallel Action-Chunk Targets"]},{"id":"stage-2","title":"Regress continuous actions","detail":"Fine-tune with absolute error on normalized targets.","column":1,"row":0,"section":"Regress continuous actions","problem_slugs":[],"planned_problems":["Measure Fine-Tuning Throughput"]},{"id":"stage-3","title":"Execute and measure throughput","detail":"Use chunks while measuring actual closed-loop timing.","column":2,"row":0,"section":"Execute and measure throughput","problem_slugs":["edge-inference-release-gate"],"planned_problems":["Compare Policy Latency Under Serving Settings"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"chunk predictions"},{"from":"stage-2","to":"stage-3","label":"trained action head"}]}
---
## Core paper explanation

OpenVLA-OFT studies a practical fine-tuning recipe: parallel action decoding, action chunks, continuous outputs, and a simple L1 objective. These changes target action-generation throughput and flexible observation/action interfaces.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Encode context and action slots

Let context $c$ include images, instruction, and any supported state input. The model predicts a chunk $\hat A=f_\theta(c)\in\mathbb R^{H\times d}$. Parallel decoding predicts action slots together instead of repeatedly invoking a token-by-token autoregressive action loop.

<!-- joint-tonic-component:stage-1 -->
- **Planned component:** Construct Parallel Action-Chunk Targets. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Regress continuous actions

For batch size $B$,
$$L_1=\frac1{BHd}\sum_{b,t,j}|\hat A_{btj}-A_{btj}|.$$
$A$ and $\hat A$ must share normalization and embodiment semantics. This objective learns conditional medians per output component; it is not an explicit multimodal action sampler like diffusion.

<!-- joint-tonic-component:stage-2 -->
- **Planned component:** Measure Fine-Tuning Throughput. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Execute and measure throughput

A useful deployment measure is $r_{\mathrm{generation}}=H/T_{\mathrm{infer}}$ actions per second, where $T_{\mathrm{infer}}$ is measured wall time. This is not the observation refresh rate or guaranteed control frequency. Specify how much of each chunk is executed before replanning and benchmark under realistic image/state input loads.

<!-- joint-tonic-component:stage-3 -->
- **Related implementation prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).
- **Planned component:** Compare Policy Latency Under Serving Settings. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

## Implement the components

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate)

Planned components: Construct Parallel Action-Chunk Targets; Measure Fine-Tuning Throughput; Compare Policy Latency Under Serving Settings. Exact approved curriculum titles are reused where available; additional named ideas require a reviewed blueprint before implementation.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Faster generation can support high-frequency manipulation. Longer chunks may still increase open-loop error, and L1 regression can average incompatible behaviors; task success and recovery matter alongside throughput.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2502.19645) · [Open-access manuscript](https://arxiv.org/pdf/2502.19645)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
