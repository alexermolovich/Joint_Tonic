# Sample an Action Trajectory with DDPM Steps

## Intuition

Reverse diffusion removes predicted corruption one level at a time. The variance of each injected random term must match the selected reverse schedule, and the final step must not add fresh noise.

## Mathematical mechanism

For forward index k, define $\alpha_k=1-\beta_k$ and $\bar\alpha_k=\prod_{j=0}^k\alpha_j$, with $\bar\alpha_{-1}=1$. The supplied prediction is $\epsilon_k\in\mathbb R^{H\times D}$. Reverse mean and variance are $$\mu_k=\frac{x_k-\beta_k\epsilon_k/\sqrt{1-\bar\alpha_k}}{\sqrt{\alpha_k}},\qquad \tilde\beta_k=\beta_k\frac{1-\bar\alpha_{k-1}}{1-\bar\alpha_k}.$$ Use $x_{k-1}=\mu_k+\sqrt{\tilde\beta_k}z_k$ for k>0. At k=0, posterior variance is zero. H is action horizon, D channel count, and z is supplied unit-noise realization.

## Visual computation trace

| Stored input index | Reverse visitation | Output trace |
|---|---|---|
| K-1 | first update | row1 |
| ... | descending | ... |
| 0 | final deterministic update | rowK |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

initial=[[1]], predicted_noise=[[[0]]], betas=[0.04], step_noise=[[[99]]] gives trace [[[1]],[[1/sqrt(0.96)]]]. Final noise is ignored even though nonzero.

## Why this matters on a robot

Swapping the forward schedule order changes the sampled trajectory. Using beta as reverse variance when the contract asks for posterior variance produces a different sampler. The stored prediction sequence is valid only for the states at which it was evaluated; this exercise does not provide a trained conditional policy.

## Physical contract and limits

Actions are normalized dimensionless controller channels; diffusion coefficients and noise are dimensionless. Diffusion indices are noise levels, not robot control timestamps; each H row denotes a future action slot. Original DDPM posterior-variance teaching sampler motivated by Diffusion Policy. A real policy recomputes its conditional denoiser on each current state; this task supplies those outputs to isolate scheduler arithmetic.

Source: [primary paper](https://arxiv.org/abs/2303.04137). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
