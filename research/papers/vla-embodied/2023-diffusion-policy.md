---
schema_version: 1
paper_id: "2023-diffusion-policy"
title: "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion"
authors:
  - "Cheng Chi"
  - "Zhenjia Xu"
  - "Siyuan Feng"
  - "Eric Cousineau"
  - "Yilun Du"
  - "Benjamin Burchfiel"
  - "Russ Tedrake"
  - "Shuran Song"
year: 2023
venue_or_status: "RSS 2023; later IJRR"
primary_url: "https://arxiv.org/abs/2303.04137"
pdf_url: "https://arxiv.org/pdf/2303.04137"
local_pdf: "./2023-diffusion-policy.pdf"
sha256: "b65c474b696a4802d8f1457d86b637ce2c5521412570d3aa928cd54563babc8f"
bytes: 6192199
pages: 19
topics:
  - "diffusion policy"
  - "visuomotor control"
  - "receding horizon"
  - "multimodal actions"
modalities:
  - "RGB images"
  - "robot state"
  - "continuous action sequences"
track_role: "core"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Diffusion Policy: Visuomotor Policy Learning via Action Diffusion

## Agent brief

Use this paper for the continuous alternative to RT-1-style action tokens. The strongest exercises isolate the forward-noising objective, conditional denoising, and receding-horizon scheduler. Keep image encoders tiny so learners can reason about the action process.

## Contribution

- **Changed:** Diffusion Policy models a conditional distribution over future action sequences rather than regressing a single average action. Iterative denoising can represent multiple valid behaviors, while action horizons and receding-horizon execution create temporal consistency for robot control.
- **Evidence:** The reported evaluation is summarized below; the proposed exercises use deterministic small-scale proxies.
- **Not established:** The paper does not establish universal safety, unsupported-embodiment robustness, or equivalence of an educational reproduction.

## Prerequisite concepts

- DDPM forward and reverse processes
- Noise schedules and timestep embeddings
- Conditional sequence models
- Receding-horizon control and closed-loop replanning

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Observation conditioner | Image/state history | Conditioning features | History order and mask are preserved | Encode a fixed observation window |
| Forward noiser | Clean chunk, timestep, noise | Noisy action chunk | Schedule coefficients broadcast exactly | Implement the closed-form sample |
| Temporal denoiser | Noisy chunk, time, condition | Noise or velocity estimate | Output shape matches the action horizon | Build a compact conditional network |
| Reverse sampler | Initial noise and denoiser | Action sequence | Terminal step and seeded noise are correct | Implement one step then the full loop |
| Horizon executor | Predicted sequence and live observations | Executed prefix and trace | Replanning respects deadlines | Simulate closed-loop execution |

## Essential equations

With clean action sequence \(A_0\), Gaussian noise \(\epsilon\), and cumulative schedule \(\bar\alpha_s\), the forward sample is

$$
A_s=\sqrt{\bar\alpha_s}A_0+\sqrt{1-\bar\alpha_s}\,\epsilon.
$$

A standard conditional noise-prediction objective is

$$
\mathcal L_{\text{diff}}=\mathbb E_{A_0,s,\epsilon}\left[\left\lVert \epsilon-\epsilon_\theta(A_s,s,h(o))\right\rVert_2^2\right].
$$

If the policy predicts \(H_p\) steps but executes \(H_a<H_p\), replanning occurs after the prefix \(\hat A_{0:H_a}\).

## Visual teaching plan

- **Denoising trajectory:** show a 2-D action path evolving from noise to a smooth multimodal command sequence.
- **Schedule explorer:** plot signal/noise coefficients across timesteps and inspect a sampled noisy chunk.
- **Horizon simulator:** adjust prediction and execution horizons while charting latency, replans, and tracking error.

## Data and evaluation

- **Reported setting and protocol:** The work spans simulated and real manipulation benchmarks with multimodal and high-dimensional action spaces. Comparisons focus on success rate and policy robustness. A learning-scale evaluation should add denoising error by timestep, sampler latency, trajectory smoothness, and closed-loop success.
- **Compute/hardware interpretation:** Reported scale and physical hardware materially affect comparability; do not infer equivalence from a toy run.
- **Educational boundary:** Use synthetic or licensed fixtures and report mechanism-level metrics separately from closed-loop outcomes.

## Limitations and failure modes

- Multiple denoising steps can violate tight control latency budgets.
- Sampler and normalization settings are part of the effective model contract.
- Offline loss is only weakly correlated with closed-loop safety.
- Stochastic outputs complicate reproducibility and regression testing.

## Implementation decomposition

1. Normalize actions and freeze the statistics as a versioned artifact.
2. Implement the beta/alpha schedule and forward sample equation.
3. Add timestep and observation conditioning to a sequence denoiser.
4. Train with a noise-prediction objective.
5. Implement a deterministic seeded sampler.
6. Wrap the sampler in a receding-horizon executor with timing metrics.

## Problem blueprints

### Problem: Forward-noise an action batch

- **Type:** function
- **Difficulty:** easy
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** clean actions, timesteps, cumulative alpha schedule, noise
- **Outputs:** noisy actions and training target
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** broadcasting, endpoint timesteps, determinism with supplied noise, numerical tolerance
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

### Problem: Perform one reverse diffusion step

- **Type:** function
- **Difficulty:** medium
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** current sample, predicted noise, schedule coefficients, optional seeded noise
- **Outputs:** previous-timestep sample
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** correct mean/variance, no noise at terminal step, batched timesteps, finite outputs
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

### Problem: Run receding-horizon inference

- **Type:** experiment
- **Difficulty:** hard
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** observation stream, sampler callback, prediction/action horizon, control deadline
- **Outputs:** executed actions, replanning trace, deadline metrics
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** horizon slicing, observation refresh, deadline accounting, deterministic seeded trace, graceful timeout fallback
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

## MLOps and deployment extensions

- Store action statistics, noise schedule, sampler steps, seed policy, and horizon settings with every checkpoint. Benchmark p50/p95 denoising latency on the target device. In shadow evaluation, replay the same observation stream across model versions and compare action distribution, smoothness, saturation, and deadline misses.

## Canonical sources

- [Primary landing page](https://arxiv.org/abs/2303.04137)
- [Open-access PDF](https://arxiv.org/pdf/2303.04137)
- [Official code or project page](https://diffusion-policy.cs.columbia.edu/)


