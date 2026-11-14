---
schema_version: 1
paper_id: "2022-smoothquant"
title: "SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models"
authors: ["Xiao, Guangxuan","Lin, Ji","Seznec, Mickael","Wu, Hao","Demouth, Julien","Han, Song"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2211.10438"
pdf_url: "https://arxiv.org/pdf/2211.10438"
local_pdf: "./2022-smoothquant.pdf"
sha256: "d17856490ff664a99f8d08fe76eabd83219ed048cd1bc18ce3d0571e71056ff8"
bytes: 5378996
pages: 13
topics: ["mlops-data-deployment","smoothquant"]
modalities: ["datasets","model-artifacts","logs","metrics"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Measure channel ranges","detail":"Collect activation and weight magnitudes on calibration data.","column":0,"row":0,"section":"Measure channel ranges","problem_slugs":[],"planned_problems":["Measure Per-Channel Activation and Weight Ranges"]},{"id":"stage-2","title":"Apply equivalent rescaling","detail":"Divide activation channels and multiply corresponding weight rows.","column":1,"row":0,"section":"Apply equivalent rescaling","problem_slugs":[],"planned_problems":["Apply an Equivalent Channel Rescaling"]},{"id":"stage-3","title":"Quantize and validate","detail":"Use integer kernels and measure end-to-end accuracy and latency.","column":2,"row":0,"section":"Quantize and validate","problem_slugs":["edge-inference-release-gate"],"planned_problems":["Quantize Weights and Activations to Int8","Validate Layer Output Error After Smoothing"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"channel scales"},{"from":"stage-2","to":"stage-3","label":"smoothed layers"}]}
---

## Core paper explanation

SmoothQuant makes activation quantization easier by moving channel-wise scale into weights through an equivalent linear-layer transformation. Calibration determines the rescaling before low-bit weight-and-activation inference.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Measure channel ranges

For $X\in\mathbb R^{N\times C}$ and $W\in\mathbb R^{C\times D}$, channel maxima are $a_j=\max_i|X_{ij}|$ and $w_j=\max_k|W_{jk}|$. A smoothing scale is
$$s_j=a_j^\alpha/w_j^{1-\alpha},\qquad 0\le\alpha\le1.$$
Zero channels require a declared numerical guard. Calibration must represent the deployment activation distribution.


**Component practice**

- Measure Per-Channel Activation and Weight Ranges — unreviewed idea; contract and evaluator required.

### Apply equivalent rescaling

With diagonal $S=\operatorname{diag}(s)$,
$$XW=(XS^{-1})(SW).$$
This identity is exact in real arithmetic before quantization. It transfers dynamic range from activations to weights without changing the intended linear function; scales can be fused into neighboring operations where valid.


**Component practice**

- Apply an Equivalent Channel Rescaling — unreviewed idea; contract and evaluator required.

### Quantize and validate

After quantization, $\hat Y=Q(XS^{-1})Q(SW)$ generally differs from $XW$. Evaluate output error, downstream task quality, memory, and target-hardware latency. A mathematically equivalent preprocessing transform does not imply lossless low-bit inference.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Quantize Weights and Activations to Int8 — unreviewed idea; contract and evaluator required.
- Validate Layer Output Error After Smoothing — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).

**Planned component problems:**

- Measure Per-Channel Activation and Weight Ranges — unreviewed idea; contract and evaluator required.
- Apply an Equivalent Channel Rescaling — unreviewed idea; contract and evaluator required.
- Quantize Weights and Activations to Int8 — unreviewed idea; contract and evaluator required.
- Validate Layer Output Error After Smoothing — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Quantization can make a VLM backbone practical on an edge device. Rare visual or language inputs may create activation outliers absent from calibration; task-specific regression tests should include those slices.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2211.10438) · [Open-access manuscript](https://arxiv.org/pdf/2211.10438)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
