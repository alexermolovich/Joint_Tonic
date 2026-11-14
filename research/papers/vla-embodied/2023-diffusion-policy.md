---
schema_version: 1
paper_id: 2023-diffusion-policy
title: 'Diffusion Policy: Visuomotor Policy Learning via Action Diffusion'
authors:
  - Cheng Chi
  - Zhenjia Xu
  - Siyuan Feng
  - Eric Cousineau
  - Yilun Du
  - Benjamin Burchfiel
  - Russ Tedrake
  - Shuran Song
year: 2023
venue_or_status: RSS 2023; later IJRR
primary_url: 'https://arxiv.org/abs/2303.04137'
pdf_url: 'https://arxiv.org/pdf/2303.04137'
local_pdf: ./2023-diffusion-policy.pdf
sha256: b65c474b696a4802d8f1457d86b637ce2c5521412570d3aa928cd54563babc8f
bytes: 6192199
pages: 19
topics:
  - diffusion policy
  - visuomotor control
  - receding horizon
  - multimodal actions
modalities:
  - RGB images
  - robot state
  - continuous action sequences
track_role: core
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: From observations to a denoised action chunk
  description: >-
    Training constructs noisy demonstrations and learns to predict their noise.
    Inference starts from fresh noise, repeatedly denoises, and executes only a
    short action prefix before observing again.
  nodes:
    - id: observation-context
      title: Encode observations
      detail: >-
        Images and robot state become conditioning features shared across the
        denoising steps.
      column: 0
      row: 0
      section: Observation conditioning
      problem_slugs: []
      planned_problems:
        - Encode Synchronized Observations for an Action Denoiser
    - id: forward-noising
      title: Noise a demonstration
      detail: >-
        Gather one cumulative schedule value per batch item and broadcast over
        the action horizon.
      column: 0
      row: 1
      section: Forward noising
      problem_slugs:
        - diffusion-action-noising
      planned_problems: []
    - id: conditional-denoiser
      title: Predict the noise
      detail: >-
        A conditional network receives a noisy action chunk, diffusion index,
        and observation features.
      column: 1
      row: 0
      section: Conditional denoiser
      problem_slugs: []
      planned_problems:
        - Build a Conditional Action Denoiser
    - id: training-loss
      title: Fit the denoiser
      detail: >-
        Training compares predicted noise with the noise used to corrupt the
        demonstration.
      column: 1
      row: 1
      section: Training objective
      problem_slugs:
        - diffusion-conditional-noise-loss
      planned_problems: []
    - id: reverse-sampling
      title: Denoise an action chunk
      detail: >-
        Inference starts from Gaussian noise and applies the trained network
        through the reverse schedule.
      column: 2
      row: 0
      section: Reverse sampling
      problem_slugs:
        - diffusion-ddpm-action-sampler
      planned_problems: []
    - id: receding-horizon
      title: Execute and replan
      detail: >-
        Execute a short valid prefix, capture new observations, and plan the
        next overlapping chunk.
      column: 2
      row: 1
      section: Receding-horizon execution
      problem_slugs:
        - diffusion-receding-horizon-window
        - diffusion-denoising-budget
      planned_problems: []
  edges:
    - from: observation-context
      to: conditional-denoiser
      label: context
    - from: forward-noising
      to: conditional-denoiser
      label: noisy actions
    - from: conditional-denoiser
      to: training-loss
      label: predicted noise
    - from: forward-noising
      to: training-loss
      label: target noise
    - from: conditional-denoiser
      to: reverse-sampling
      label: trained network
    - from: reverse-sampling
      to: receding-horizon
      label: action chunk
---
## Core paper explanation

A robot often has several reasonable ways to act from the same observation. Averaging those demonstrations can produce a command that follows none of them. Diffusion Policy represents a conditional distribution over **whole action sequences**: it learns to remove noise from demonstrated sequences, then uses the learned denoiser to generate a coherent future chunk. Images and robot state condition the prediction; a receding-horizon controller executes a short prefix and replans from fresh observations.

The paper studies convolutional and transformer denoisers, observation conditioning, and temporal execution. The runnable Joint Tonic component, [Add Noise to an Action Sequence](/problems/diffusion-action-noising), isolates the forward process used to build training examples. It does not train a policy, implement a reverse sampler, or establish closed-loop task success.

## Execution flow

The graph separates **training** from **inference**. Training pairs observation context with a clean demonstration, constructs a noisy chunk, predicts its noise, and updates network weights. Inference reuses those trained weights to turn fresh noise into an action chunk. Only the selected action prefix reaches the controller; subsequent observations start a new planning cycle. The diffusion index is a model-noise level, not a robot timestamp.

### Observation conditioning

At control time $t$, let $O_t$ contain the most recent $H_o$ observations. An observation can include camera images and a proprioceptive state such as joint positions. An encoder produces conditioning features

$$
c_t=g_\phi(O_t).
$$

The particular shape of $c_t$ depends on the denoiser architecture: it may be a feature vector or a sequence of visual/state tokens. It must preserve batch alignment with its demonstrated action chunk. Cache the observation features across reverse-diffusion steps for the same planning cycle; a new real observation requires new features.

An action chunk $A^{(0)}\in\mathbb R^{B\times H_p\times D}$ has batch size $B$, prediction horizon $H_p$, and $D$ action channels. The superscript denotes diffusion level; the horizon index denotes future control steps. Action units and frames are inherited from the dataset and controller. If actions are normalized, the checkpoint must carry the inverse normalization and the original channel meanings.

<!-- joint-tonic-component:observation-context -->
- **Planned component:** Encode Synchronized Observations for an Action Denoiser. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Forward noising

Choose variance increments $\beta_k\in(0,1)$, define $\alpha_k=1-\beta_k$, and accumulate

$$
\bar\alpha_k=\prod_{j=1}^{k}\alpha_j.
$$

For independent standard-normal noise $E$ of the same shape as the action chunk, the closed-form corruption is

$$
A^{(k)}=\sqrt{\bar\alpha_k}\,A^{(0)}
+\sqrt{1-\bar\alpha_k}\,E.
$$

The signal and noise coefficients have squared sum one. Increasing the noise level changes both the amount of retained motion and the prediction problem presented to the network. This formula builds a training sample directly; it does not require executing every intermediate noise step.

**Implement this stage:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising). Its contract supplies $E$ and one diffusion index $k_b$ per batch item rather than sampling internally. Gather $\bar\alpha_{k_b}$ into shape $(B,1,1)$ so that it broadcasts across horizon and action channels. With validity mask $M\in\{0,1\}^{B\times H_p}$, the exercise returns

$$
\widetilde A^{(k)}_{bhd}=M_{bh}A^{(k_b)}_{bhd},
\qquad
\widetilde E_{bhd}=M_{bh}E_{bhd}.
$$

The padding mask is part of the educational batching contract. It prevents padded action slots from becoming training targets; it is not a collision or robot-safety mask.

<!-- joint-tonic-component:forward-noising -->
- **Implement this component:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising).
<!-- /joint-tonic-component -->

### Conditional denoiser

The network receives the corrupted chunk, its diffusion level, and the observation context:

$$
\widehat E=\epsilon_\theta(A^{(k)},k,c_t),
\qquad
\widehat E\in\mathbb R^{B\times H_p\times D}.
$$

The noise-level embedding tells the network how strongly the input was corrupted. Observation conditioning tells it which actions are plausible now. Predicting an entire sequence lets the network represent dependencies across action times; independently generating each command would discard that temporal structure. A low-dimensional action channel and a camera pixel are not interchangeable tokens: their units, normalization, and temporal alignment must remain explicit.

<!-- joint-tonic-component:conditional-denoiser -->
- **Planned component:** Build a Conditional Action Denoiser. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Training objective

For the usual noise-prediction parameterization, a batch objective compares the known corruption noise with the predicted noise. With the teaching problem's mask, the normalized form is

$$
\mathcal L_{\mathrm{noise}}=
\frac{\sum_{b,h,d}M_{bh}(E_{bhd}-\widehat E_{bhd})^2}
{D\sum_{b,h}M_{bh}}.
$$

This expression assumes at least one valid horizon slot; an all-padding batch must be rejected or explicitly skipped. The target is $E$, not the corrupted action and not the clean action. Training averages this loss over demonstrations, sampled noise, and diffusion indices. The forward-noising exercise prepares the input/target pair; the linked noise-loss exercise evaluates this objective with supplied predictions. Training a complete conditional denoiser and optimizing its parameters remain outside those bounded exercises.

<!-- joint-tonic-component:training-loss -->
- **Implement this component:** [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss).
<!-- /joint-tonic-component -->

### Reverse sampling

At inference, initialize an action chunk $A^{(K)}\sim\mathcal N(0,I)$. A standard DDPM noise-prediction update is

$$
A^{(k-1)}=
\frac{1}{\sqrt{\alpha_k}}
\left(A^{(k)}-
\frac{1-\alpha_k}{\sqrt{1-\bar\alpha_k}}
\epsilon_\theta(A^{(k)},k,c_t)\right)
+\sigma_k Z_k,
$$

where $Z_k$ is fresh standard-normal noise and $\sigma_k$ is set by the chosen reverse schedule. The final step normally omits stochastic noise. This is a clear reference parameterization, not a requirement to use this sampler for every Diffusion Policy deployment: accelerated sampling schedules can change the update and number of network calls. Sampler, schedule, prediction type, and checkpoint must agree.

<!-- joint-tonic-component:reverse-sampling -->
- **Implement this bounded component:** [Sample an Action Trajectory with DDPM Steps](/problems/diffusion-ddpm-action-sampler). See its contract for deliberate teaching simplifications.
<!-- /joint-tonic-component -->

### Receding-horizon execution

Let $H_a\le H_p$ be the number of newly planned actions executed before replanning. After selecting the chunk positions aligned with the current control time, execute that prefix and observe again. With control interval $\Delta t$ seconds, the replanning interval is approximately

$$
T_{\mathrm{replan}}=H_a\Delta t.
$$

For $H_p=16$, $H_a=4$, and $\Delta t=0.05$ seconds, the action chunk spans $0.8$ seconds while replanning occurs every $0.2$ seconds. Smaller execution horizons provide faster feedback but require more frequent inference. Real execution also needs an explicit latency policy: stale actions must not be treated as if they were generated from the latest camera frame.

<!-- joint-tonic-component:receding-horizon -->
- **Implement this component:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window).
- **Implement this bounded component:** [Budget Denoising Steps Against Control Frequency](/problems/diffusion-denoising-budget). See its contract for deliberate teaching simplifications.
<!-- /joint-tonic-component -->

## Worked tensor example

Consider one valid action entry with clean value $2$, supplied noise $4$, and cumulative signal coefficient $\bar\alpha=0.5$. The forward sample is

$$
\sqrt{0.5}\,2+\sqrt{0.5}\,4
=4.242640687\ldots,
\qquad E_{\mathrm{target}}=4.
$$

If the corresponding horizon slot is padding, the exercise returns zero for both the noised entry and its target. A different batch item may use a different schedule index without changing the $(B,H_p,D)$ output shape. [Implement and test these cases](/problems/diffusion-action-noising).

## Why this matters on a robot

Action-sequence generation can represent multimodal demonstrations while keeping adjacent commands coordinated. Its practical benefit depends on the entire observation-to-actuation path. A normalization mismatch changes the physical command represented by every number. A swapped action frame rotates or translates the intended motion. A slow sampler can deliver a smooth but obsolete plan. Evaluate action error, closed-loop task success, inference tail latency, and recovery under changed observations separately; a small noise-loss value alone is insufficient.

## Implement the components

- [Sample an Action Trajectory with DDPM Steps](/problems/diffusion-ddpm-action-sampler)
- [Budget Denoising Steps Against Control Frequency](/problems/diffusion-denoising-budget)

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Add Noise to an Action Sequence](/problems/diffusion-action-noising)
- [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss)
- [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window)

Remaining proposed components: Encode Synchronized Observations for an Action Denoiser; Build a Conditional Action Denoiser. These are not published exercises; source preparation and a reviewed blueprint are still required.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Sources and scope

[Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137) · [Open-access manuscript](https://arxiv.org/pdf/2303.04137) · [Official project](https://diffusion-policy.cs.columbia.edu/)

This explanation uses original wording and explicit notation for the core mechanisms. The masking convention and worked scalar fixture follow Joint Tonic's published problem contract. They are teaching choices, not a claim to reproduce the paper's datasets, model scale, or closed-loop results. The local PDF remains a research reference under the provenance terms in its metadata.
