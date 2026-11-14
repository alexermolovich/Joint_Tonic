---
schema_version: 1
paper_id: 2022-smoothquant
title: >-
  SmoothQuant: Accurate and Efficient Post-Training Quantization for Large
  Language Models
authors:
  - 'Xiao, Guangxuan'
  - 'Lin, Ji'
  - 'Seznec, Mickael'
  - 'Wu, Hao'
  - 'Demouth, Julien'
  - 'Han, Song'
year: 2022
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2211.10438'
pdf_url: 'https://arxiv.org/pdf/2211.10438'
local_pdf: ./2022-smoothquant.pdf
sha256: d17856490ff664a99f8d08fe76eabd83219ed048cd1bc18ce3d0571e71056ff8
bytes: 5378996
pages: 13
topics:
  - mlops-data-deployment
  - smoothquant
modalities:
  - datasets
  - model-artifacts
  - logs
  - metrics
track_role: supporting
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Follow the data through the mechanism. Training objectives and inference
    behavior are distinguished in the linked explanations.
  nodes:
    - id: stage-1
      title: Measure channel ranges
      detail: Collect activation and weight magnitudes on calibration data.
      column: 0
      row: 0
      section: Measure channel ranges
      problem_slugs:
        - smoothquant-channel-ranges
      planned_problems: []
    - id: stage-2
      title: Apply equivalent rescaling
      detail: Divide activation channels and multiply corresponding weight rows.
      column: 1
      row: 0
      section: Apply equivalent rescaling
      problem_slugs:
        - smoothquant-equivalent-rescaling
      planned_problems: []
    - id: stage-3
      title: Quantize and validate
      detail: Use integer kernels and measure end-to-end accuracy and latency.
      column: 2
      row: 0
      section: Quantize and validate
      problem_slugs:
        - edge-inference-release-gate
        - smoothquant-int8-linear-layer
        - smoothquant-layer-error-report
        - smoothquant-calibrated-layer-integration
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: channel scales
    - from: stage-2
      to: stage-3
      label: smoothed layers
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

- Runnable component: [Measure Per-Channel Activation and Weight Ranges](/problems/smoothquant-channel-ranges). Uses the bounded contract; no full paper reproduction is claimed.

### Apply equivalent rescaling

With diagonal $S=\operatorname{diag}(s)$,
$$XW=(XS^{-1})(SW).$$
This identity is exact in real arithmetic before quantization. It transfers dynamic range from activations to weights without changing the intended linear function; scales can be fused into neighboring operations where valid.


**Component practice**

- Runnable component: [Apply an Equivalent Channel Rescaling](/problems/smoothquant-equivalent-rescaling). Uses the bounded contract; no full paper reproduction is claimed.

### Quantize and validate

After quantization, $\hat Y=Q(XS^{-1})Q(SW)$ generally differs from $XW$. Evaluate output error, downstream task quality, memory, and target-hardware latency. A mathematically equivalent preprocessing transform does not imply lossless low-bit inference.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Runnable component: [Quantize Weights and Activations to Int8](/problems/smoothquant-int8-linear-layer). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Validate Layer Output Error After Smoothing](/problems/smoothquant-layer-error-report). Uses the bounded contract; no full paper reproduction is claimed.

- Runnable integration: [Calibrate and Evaluate a Smoothed Int8 Layer](/problems/smoothquant-calibrated-layer-integration). Composes calibration-only ranges, guarded smoothing, simulated int8 arithmetic and separate validation diagnostics; configuration selection does not filter by the absolute release gate.

## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Runnable component:** [Measure Per-Channel Activation and Weight Ranges](/problems/smoothquant-channel-ranges).
- **Runnable component:** [Apply an Equivalent Channel Rescaling](/problems/smoothquant-equivalent-rescaling).
- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).
- **Runnable component:** [Quantize Weights and Activations to Int8](/problems/smoothquant-int8-linear-layer).
- **Runnable component:** [Validate Layer Output Error After Smoothing](/problems/smoothquant-layer-error-report).

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

Quantization can make a VLM backbone practical on an edge device. Rare visual or language inputs may create activation outliers absent from calibration; task-specific regression tests should include those slices.

The [executable paper project](/projects/2022-smoothquant) composes these operations on original synthetic layer inputs. Validation observations select a configuration and therefore are not an untouched final test set. The project omits pretrained transformers and hardware kernels.

## Scope of the runnable components

The runnable layer exercises use supplied, synthetic calibration matrices rather than a pretrained language model. [Channel ranges](/problems/smoothquant-channel-ranges) measures absolute maxima; [equivalent rescaling](/problems/smoothquant-equivalent-rescaling) consumes caller-supplied positive scales. [Int8 simulation](/problems/smoothquant-int8-linear-layer) uses symmetric [-127,127] integers, per-token activation scales, per-output weight scales and int64 accumulation. [Layer error reporting](/problems/smoothquant-layer-error-report) keeps per-row absolute failures separate from a global relative diagnostic. These numerical recipes do not reproduce every SmoothQuant kernel configuration or establish a speedup.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2211.10438) · [Open-access manuscript](https://arxiv.org/pdf/2211.10438)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
