# Balance action accuracy with a useful latent distribution

## Intuition

A demonstration may contain multiple reasonable ways to complete the same task. A conditional variational model can encode that variation in a latent vector during training. Reconstruction rewards accurate action chunks; KL regularization keeps that latent distribution close enough to a simple prior to use at inference.

## Two reductions with different meanings

Let predicted and target normalized actions be $\widehat A,A\in\mathbb R^{B\times H\times D}$, and let $V\in\{0,1\}^{B\times H}$ identify recorded targets. $B$ counts episodes, $H$ future control ticks and $D$ action channels. Define

$$
R=\frac{\sum_{b,h,d} V_{bh}|\widehat A_{bhd}-A_{bhd}|}
{D\sum_{b,h}V_{bh}}.
$$

This is a global mean over valid scalar targets. It does not give each episode equal reconstruction weight when valid lengths differ.

For posterior mean $\mu\in\mathbb R^{B\times Z}$ and log variance $\ell\in\mathbb R^{B\times Z}$, the diagonal Gaussian has variance $\exp(\ell)$. Relative to a standard-normal prior, the batch-mean KL is

$$
K=\frac{1}{2B}\sum_{b,z}\left(\mu_{bz}^2+\exp(\ell_{bz})-1-\ell_{bz}\right),
\qquad L=R+\beta K.
$$

The latent size $Z$ is summed, not averaged. $\beta\ge0$ controls this explicit tradeoff; changing Z without reconsidering beta changes the total regularization scale. Latent coordinates and normalized action errors are dimensionless.

## Visual: follow the reductions

| Tensor | Mask/reduction | Result |
|---|---|---|
| Absolute action residual, B × H × D | Mask H, sum B/H/D, divide valid scalar count | R, scalar |
| Gaussian KL terms, B × Z | Sum Z, average B, multiply 1/2 | K, scalar |
| R and K | R + beta × K | L, scalar |

The table is a static shape diagram and text alternative. The action mask does not remove latent rows.

For valid residuals [1,2], R=1.5. With mean [1,0] and log variance [0,0], the two KL summands are1 and0, so K=0.5. Beta2 gives L=2.5. This matches the public contract without training a CVAE.

## Why this matters on a robot

Padded tail actions must not pull a policy toward a zero command. Conversely, silently dropping a posterior's KL because its action mask is empty changes the batch objective. A common implementation error treats log variance as log standard deviation, doubling the exponent and giving a different loss.

ACT's paper motivates the reconstruction-plus-KL mechanism; this task makes reduction and padding choices explicit. It does not claim these small fixtures reproduce the reported robot performance.

## Check your understanding

1. Why divide reconstruction by D times the valid count? Each valid timestep contains D scalar residuals.
2. Does beta=0 justify detaching the reconstruction? No; reconstruction must train the action predictor.
3. Which posterior has zero KL? Mean zero and log variance zero.


## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2304.13705), Section IV-B: Modeling human data. Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective. The global valid-scalar reconstruction mean and batch-mean latent sum are explicit teaching reductions. No encoder, latent sampling, transformer, or training run is reproduced.

Prerequisites: [ act-sliding-action-chunks ](/problems/act-sliding-action-chunks)
