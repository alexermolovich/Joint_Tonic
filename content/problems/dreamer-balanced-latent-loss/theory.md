# Compute a Balanced Latent-Model Loss

## Intuition

The dynamics prior should learn to predict the posterior, while the posterior should become easier to predict without discarding useful information. Separate gradient paths and a free-nat floor control this tradeoff.

## Mathematical mechanism

For each row b, categorical group g and category c, convert logits into softmax probabilities s and mix in uniform support: $$q_{bgc}=0.99s^q_{bgc}+0.01/C,\qquad p_{bgc}=0.99s^p_{bgc}+0.01/C.$$ The categorical groups factorize, so their divergences add: $$K_b=\sum_{g,c}q_{bgc}(\log q_{bgc}-\log p_{bgc}).$$ The dynamics term is max(1,KL(stop(q)||p)); the representation term is max(1,KL(q||stop(p))). With valid-row count N and supplied prediction loss ell, $$L=\frac1N\sum_{b:M_b}\left[\ell_b+\max(1,K_b)+0.1\max(1,K_b)\right].$$ Equal forward values do not imply equal gradients. For a vector softmax s and upstream derivative u with respect to its uniform-mixed distribution, the logit derivative is $$\frac{\partial L}{\partial l}=0.99s\odot\left(u-\sum_c s_cu_c\right).$$ On active rows K>1, use $u_p=-q/p$ for the prior path and $u_q=\log q-\log p+1$ for the posterior path, multiplying by 1/N and .1/N respectively. K<=1 and invalid rows have zero KL gradients. This analytical contract isolates the two stop-gradient paths; no latent sampler is included.

## Visual computation trace

| KL regime | Dynamics prior gradient | Representation posterior gradient |
|---|---|---|
| K<=1 nat | zero | zero |
| K>1 nat | full coefficient 1 | coefficient 0.1 |
| Missing row | zero | zero |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Both categorical logits [0,0], one group, prediction_loss 2, valid True -> K=0, loss=3.1, both logit gradients 0,prediction_gradient 1.

## Why this matters on a robot

Errors in learned contact dynamics or termination predictions can compound through an imagined horizon. A numerically correct return remains conditional on those supplied predictions.

## Physical contract and limits

Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats. Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion. A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

Source: [primary paper](https://arxiv.org/html/2301.04104v2). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
