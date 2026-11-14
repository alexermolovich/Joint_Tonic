---
schema_version: 1
paper_id: 2024-openvla
title: 'OpenVLA: An Open-Source Vision-Language-Action Model'
authors:
  - Moo Jin Kim et al.
year: 2024
venue_or_status: CoRL 2024
primary_url: 'https://arxiv.org/abs/2406.09246'
pdf_url: 'https://arxiv.org/pdf/2406.09246'
local_pdf: ./2024-openvla.pdf
sha256: 353c37df34458f12f969b14dfd8b77175b727b9cddea7bb891759beddeefe1be
bytes: 13240309
pages: 37
topics:
  - open VLA
  - visual feature fusion
  - action tokenization
  - efficient fine-tuning
modalities:
  - RGB images
  - language instructions
  - discrete action tokens
track_role: advanced
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Aligned visual feature streams are fused into language-model context,
    action-token predictions are decoded using training-set normalization, and
    adaptation/serving preserve that interface.
  nodes:
    - id: stage-1
      title: Fuse visual representations
      detail: >-
        Align complementary visual feature streams and project them into
        language context.
      column: 0
      row: 0
      section: Fuse visual representations
      problem_slugs:
        - openvla-fuse-visual-streams
      planned_problems: []
    - id: stage-2
      title: Quantize and predict actions
      detail: Use uniform bins within robust per-channel action bounds.
      column: 1
      row: 0
      section: Quantize and predict actions
      problem_slugs:
        - rt1-action-codec
        - openvla-training-quantile-action-bins
        - openvla-action-token-training-batch
      planned_problems: []
    - id: stage-3
      title: Adapt and serve consistently
      detail: >-
        Preserve visual preprocessing, tokenizer mapping, action statistics, and
        compute constraints.
      column: 2
      row: 0
      section: Adapt and serve consistently
      problem_slugs:
        - edge-inference-release-gate
        - openvla-lora-policy-layer
        - openvla-quantized-serving-budget
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: visual-language context
    - from: stage-2
      to: stage-3
      label: trained policy
---
## Core paper explanation

OpenVLA joins pretrained visual representations with a language model and fine-tunes it to predict discretized robot actions. It combines visual features from complementary encoders and exposes practical fine-tuning and serving tradeoffs for a large VLA. Its action representation uses uniform bins inside robust, dataset-derived bounds. Those bounds are percentile-based; the bins themselves are not equal-probability quantile bins.

## Execution flow

Aligned visual feature streams are fused into language-model context, action-token predictions are decoded using training-set normalization, and adaptation/serving preserve that interface.

### Fuse visual representations

Suppose the two encoders produce spatially aligned features $F_1\in\mathbb R^{N\times d_1}$ and $F_2\in\mathbb R^{N\times d_2}$. Feature concatenation and projection can be written

$$
Z=P([F_1;F_2]_{\mathrm{feature}})\in\mathbb R^{N\times d_{\mathrm{LM}}}.
$$

The concatenation is along feature width, not the token axis. Equal token counts are insufficient if the two preprocessing pipelines associate those tokens with different image patches. The projected visual sequence then conditions the language backbone alongside the instruction.

<!-- joint-tonic-component:stage-1 -->
- **Implement this bounded component:** [Fuse Two Visual Feature Streams Safely](/problems/openvla-fuse-visual-streams). See its contract for deliberate teaching simplifications.
<!-- /joint-tonic-component -->

### Quantize and predict actions

For action channel $j$, let $l_j=Q_{0.01}(A_j)$ and $u_j=Q_{0.99}(A_j)$ be training-set percentile bounds. With $K=256$ bins,

$$
q_j=\operatorname{clip}\left(\left\lfloor K\frac{a_j-l_j}{u_j-l_j}\right\rfloor,0,K-1\right),
\qquad \Delta_j=\frac{u_j-l_j}{K}.
$$

Every bin has the same width $\Delta_j$ within a channel. Outliers are clipped instead of expanding the interval. [Quantize and Decode Robot Actions](/problems/rt1-action-codec) implements the uniform-codec mechanism with supplied bounds; deriving robust bounds and binding IDs to OpenVLA’s tokenizer are additional steps. Training predicts serialized action tokens with cross-entropy:

$$
\mathcal L=-\sum_i\log p_\theta(\tau_i\mid I,c,\tau_{<i}).
$$

<!-- joint-tonic-component:stage-2 -->
- **Related implementation prerequisite:** [Quantize and Decode Robot Actions](/problems/rt1-action-codec).
- **Implement this bounded component:** [Quantize Actions from Training-Set Quantiles](/problems/openvla-training-quantile-action-bins). See its contract for deliberate teaching simplifications.
- **Implement this bounded component:** [Build a VLA Action-Token Training Batch](/problems/openvla-action-token-training-batch). See its contract for deliberate teaching simplifications.
<!-- /joint-tonic-component -->

### Adapt and serve consistently

A low-rank adaptation of a weight matrix $W\in\mathbb R^{d_o\times d_i}$ can use

$$
W'=W+\frac{\alpha}{r}BA,
\qquad A\in\mathbb R^{r\times d_i},\quad B\in\mathbb R^{d_o\times r}.
$$

This adds $r(d_i+d_o)$ trainable entries rather than updating all $d_od_i$ entries. It is a parameterization of fine-tuning, not an automatic latency reduction: merged weights and serving kernels determine inference cost. [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate) is a related component for evaluating a candidate configuration against measured constraints.

<!-- joint-tonic-component:stage-3 -->
- **Related implementation prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).
- **Implement this bounded component:** [Add Low-Rank Adaptation to a Policy Layer](/problems/openvla-lora-policy-layer). See its contract for deliberate teaching simplifications.
- **Implement this bounded component:** [Estimate Memory, Latency, and Quantized Serving Budgets](/problems/openvla-quantized-serving-budget). See its contract for deliberate teaching simplifications.
<!-- /joint-tonic-component -->

## Implement the components

- [Fuse Two Visual Feature Streams Safely](/problems/openvla-fuse-visual-streams)
- [Quantize Actions from Training-Set Quantiles](/problems/openvla-training-quantile-action-bins)
- [Build a VLA Action-Token Training Batch](/problems/openvla-action-token-training-batch)
- [Add Low-Rank Adaptation to a Policy Layer](/problems/openvla-lora-policy-layer)
- [Estimate Memory, Latency, and Quantized Serving Budgets](/problems/openvla-quantized-serving-budget)

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Quantize and Decode Robot Actions](/problems/rt1-action-codec)
- [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate)

All components currently named in this paper’s curriculum tree have a runnable bounded exercise. This does not reproduce the complete paper or its headline results.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

A change to action normalization changes the meaning of generated tokens even if model weights stay fixed. New camera views, gripper conventions, or control rates can also break transfer. Fine-tuning and quantized serving should be evaluated on closed-loop tasks as well as memory, latency, and offline action error.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2406.09246) · [Open-access manuscript](https://arxiv.org/pdf/2406.09246)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
