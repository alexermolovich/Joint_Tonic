# Update a Temperature Objective (later SAC extension)

## Intuition

The entropy temperature should increase when the sampled policy is less random than the declared target and decrease when it is more random. Updating log temperature preserves positivity, while explicit clipping bounds this teaching update.

## Mathematical mechanism

Let $\lambda=\log\alpha$ and target entropy $H_*$ in nats. Holding sampled log densities ell fixed, $$J(\lambda)=-e^\lambda\operatorname{mean}_{valid}(\ell+H_*),\quad \frac{dJ}{d\lambda}=J(\lambda),\quad\lambda^+=\operatorname{clip}(\lambda-\eta J,-20,5).$$ Eta is the supplied step size. Measured entropy is minus mean log density. This exact exponential objective is specified explicitly rather than silently replacing exp(lambda) by lambda.

## Visual computation trace

| Measured entropy | Target | Initial alpha | Gradient | Effect |
|---|---|---|---|---|
| 2 | 1 | 1 | +1 | reduce alpha |
| 0 | 1 | 1 | -1 | increase alpha |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

log_alpha0, logp[[-2]], validTrue, target_entropy1, learning_rate.1 returns loss1, gradient1, log_alpha-.1, alpha=exp(-.1).

## Why this matters on a robot

A robot learning pipeline depends on correct action likelihoods, terminal flags and dataset identity. A numerically small loss cannot repair incorrect replay semantics or absent action coverage.

## Physical contract and limits

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

Source: [primary paper](https://arxiv.org/abs/1801.01290). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.

Automatic temperature tuning is the later [SAC Algorithms and Applications extension](https://arxiv.org/abs/1812.05905), not the fixed-temperature original paper.
