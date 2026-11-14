---
schema_version: 1
paper_id: 2023-aloha-act
title: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware
authors:
  - Tony Z. Zhao
  - Vikash Kumar
  - Sergey Levine
  - Chelsea Finn
year: 2023
venue_or_status: RSS 2023
primary_url: 'https://arxiv.org/abs/2304.13705'
pdf_url: 'https://arxiv.org/pdf/2304.13705'
local_pdf: ./2023-aloha-act.pdf
sha256: 2e2fe25860f5f9cee9e655a2714e9f2264a7a5078bcd267c16d3f39af461345a
bytes: 5353485
pages: 18
topics:
  - action chunking
  - bimanual manipulation
  - imitation learning
  - conditional VAE
modalities:
  - multi-camera RGB
  - joint state
  - bimanual actions
track_role: core
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Training encodes a demonstrated action chunk into a latent variable. The
    policy decodes a future chunk, and inference combines overlapping
    predictions for the current control time. The demonstration encoder is not
    required to consume future actions at deployment.
  nodes:
    - id: stage-1
      title: Encode demonstration variation
      detail: >-
        During training, infer a latent distribution from the demonstrated
        chunk.
      column: 0
      row: 0
      section: Encode demonstration variation
      problem_slugs:
        - act-sliding-action-chunks
        - act-teleoperation-quality
      planned_problems: []
    - id: stage-2
      title: Decode an action chunk
      detail: >-
        Predict a sequence and train with reconstruction plus latent
        regularization.
      column: 1
      row: 0
      section: Decode an action chunk
      problem_slugs:
        - act-cvae-loss
      planned_problems: []
    - id: stage-3
      title: Ensemble overlapping predictions
      detail: Average predictions made for the same physical control time.
      column: 2
      row: 0
      section: Ensemble overlapping predictions
      problem_slugs:
        - act-temporal-ensembling
        - act-chunk-compounding-error
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: latent and observation
    - from: stage-2
      to: stage-3
      label: overlapping chunks
---
## Core paper explanation

ACT predicts a short future sequence of actions from observations instead of one action at a time. This action chunking helps model temporally correlated demonstrations. A conditional variational autoencoder represents variation in demonstrated action sequences, and temporal ensembling combines overlapping predictions for the same control time. ALOHA provides the low-cost bimanual hardware and demonstration setup used to study this learning method.

## Execution flow

Training encodes a demonstrated action chunk into a latent variable. The policy decodes a future chunk, and inference combines overlapping predictions for the current control time. The demonstration encoder is not required to consume future actions at deployment.

### Encode demonstration variation

For demonstration chunk $A\in\mathbb R^{H\times D}$ and conditioning state $o$, let

$$
q_\phi(z\mid A,o)=\mathcal N(\mu,\operatorname{diag}(\sigma^2)),
\qquad z=\mu+\sigma\odot\epsilon,\quad\epsilon\sim\mathcal N(0,I).
$$

The reparameterization makes gradients flow through $\mu$ and $\sigma$. The latent describes variation in the demonstration; it is not an extra measurement available from the robot. The encoder’s training inputs must not leak future target actions into the deployed policy path.

<!-- joint-tonic-component:stage-1 -->
- **Implement this component:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks).
- **Implement this bounded component:** [Detect Teleoperation Demonstration Quality Failures](/problems/act-teleoperation-quality). See its contract for deliberate teaching simplifications.
<!-- /joint-tonic-component -->

### Decode an action chunk

The decoder produces $\hat A=f_\theta(o,z)$. A reconstruction-plus-KL objective is

$$
\mathcal L=\|A-\hat A\|_1+
\frac{\beta}{2}\sum_j\left(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2\right).
$$

The KL expression compares a diagonal Gaussian with $\mathcal N(0,I)$. A batched implementation must define its reduction and exclude padding according to its contract. The paper uses the latent’s prior mean for deterministic inference. Each action entry retains the robot controller’s joint/pose convention; chunk index is a future control step, not a diffusion step.

<!-- joint-tonic-component:stage-2 -->
- **Implement this component:** [Compute a Masked CVAE Reconstruction and KL Loss](/problems/act-cvae-loss).
<!-- /joint-tonic-component -->

### Ensemble overlapping predictions

Suppose multiple chunks predict the action for time $t$. Index those predictions by $i=0,1,\ldots$ from oldest to newest. The paper’s weighting convention is

$$
w_i=e^{-mi},\qquad
\bar a_t=\frac{\sum_iw_i\hat a_t^{(i)}}{\sum_iw_i},\quad m\ge0.
$$

Here $w_0$ belongs to the oldest prediction. Increasing $m$ therefore increases preference for older predictions; changing the indexing reverses that behavior. This averages estimates for the same target time, not neighboring actions along one trajectory. Averaging neighboring physical times would introduce a different smoothing delay.

<!-- joint-tonic-component:stage-3 -->
- **Implement this component:** [Blend Overlapping Action Chunks with Temporal Ensembling](/problems/act-temporal-ensembling).
- **Implement this bounded component:** [Evaluate Chunk Length Against Compounding Error](/problems/act-chunk-compounding-error). See its contract for deliberate teaching simplifications.
<!-- /joint-tonic-component -->

## Implement the components

- [Detect Teleoperation Demonstration Quality Failures](/problems/act-teleoperation-quality)
- [Evaluate Chunk Length Against Compounding Error](/problems/act-chunk-compounding-error)

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks)
- [Compute a Masked CVAE Reconstruction and KL Loss](/problems/act-cvae-loss)
- [Blend Overlapping Action Chunks with Temporal Ensembling](/problems/act-temporal-ensembling)

All components currently named in this paper’s curriculum tree have a runnable bounded exercise. This does not reproduce the complete paper or its headline results.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Chunking reduces repeated one-step prediction errors but creates a responsiveness tradeoff. Temporal alignment is essential: mixing predictions for different target times can produce lag even when array shapes agree. Bimanual demonstrations also require synchronized observations and consistent joint ordering.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2304.13705) · [Open-access manuscript](https://arxiv.org/pdf/2304.13705)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
