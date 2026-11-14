# Corrupting a trajectory in a controlled way

## Intuition

A clean action chunk describes coordinated motion over several future steps. The forward process blends it with known noise. Early schedule positions retain more motion structure; late positions can look almost random. The denoiser's supervised target is the particular noise used to create that input.

## Mathematics and tensor axes

Let A_0 be a B×H×D clean action tensor and E a noise tensor of the same shape. A cumulative signal coefficient ᾱ_t lies in [0,1]. Each batch item can use a different timestep.

$$
A_t=\sqrt{\bar\alpha_t}\,A_0+
\sqrt{1-\bar\alpha_t}\,E.
$$

The noise prediction target is E, regardless of t. A later learning problem could minimize:

$$
\mathcal L_{\text{noise}}=
\frac{1}{|\Omega|}\sum_{(b,h,d)\in\Omega}
\left(E_{bhd}-\hat E_{bhd}\right)^2,
$$

where Ω contains valid, unpadded entries. This exercise constructs the inputs and targets; it does not calculate the model loss.

The square roots matter. The coefficients' squared sum is one. Using ᾱ directly as the signal weight changes the noise schedule. alpha_bar already contains cumulative products, so do not cumulatively multiply it again.

## Visual lesson

The diffusion visual plots one action channel over the horizon. A schedule slider changes the blend of clean motion and noise. A batch selector demonstrates that each trajectory can choose its own timestep. Invalid padded positions are shaded and excluded from the linked numerical table. A table view supplies values and coefficients without animation.

## Worked example

With clean action 2, noise 4 and ᾱ=0.5, the result is sqrt(0.5)×2 + sqrt(0.5)×4 ≈4.242641. The target stays 4. If that step is padding, both returned entries become zero.

## Why this matters on a robot

A train/serve normalization mismatch changes the meaning of every noised action. Padding errors can teach the model to imitate synthetic zeros as real commands. A schedule, action normalization artifact, control period and horizon definition all belong with the checkpoint.

## Failure modes and scope

A (B,) schedule vector does not automatically broadcast over a (B,H,D) tensor as intended; reshape it to (B,1,1). Sampling fresh noise inside this function breaks reproducibility. Returning detached tensors breaks upstream differentiation.

[Diffusion Policy](https://arxiv.org/abs/2303.04137) motivates action-sequence diffusion. The supplied schedule and noise let this lesson isolate the forward mechanism without claiming closed-loop robot performance.
