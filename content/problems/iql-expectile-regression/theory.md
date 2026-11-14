# Compute an Expectile Regression Loss

## Intuition

An expectile emphasizes one side of a squared residual. In IQL, weighting higher observed action values more strongly can raise the state-value estimate without querying actions absent from the offline dataset.

## Mathematical mechanism

Every input tensor in the equation has shape (B,T): B is the number of independent streams and T the number of samples. $M_{bt}$ is the Boolean validity mask; masked entries contribute zero.

For target Q and value V, let $u=Q-V$ and $w(u)=\tau$ for $u\ge0$, otherwise $1-\tau$. Then $$L=\frac{\sum M w(u)u^2}{N},\qquad\nabla_V L=-\frac{2M w(u)u}{N},\quad N=\sum M.$$ Tau is dimensionless; Q,V,u use reward units and the loss uses squared reward units. Empty support has zero loss and gradient. No quantile sorting or unseen-action maximization is involved.

## Visual computation trace

| Residual | tau | Weight | Squared weighted term |
|---|---|---|---|
| +1 | 0.75 | 0.75 | 0.75 |
| -1 | 0.75 | 0.25 | 0.25 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Q=[[2,0]], V=[[1,1]], both valid, tau.75 gives loss.5, per_element[[.75,.25]], value_gradient[[-.75,.25]].

## Why this matters on a robot

A robot learning pipeline depends on correct action likelihoods, terminal flags and dataset identity. A numerically small loss cannot repair incorrect replay semantics or absent action coverage.

## Physical contract and limits

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

Source: [primary paper](https://arxiv.org/abs/2110.06169). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
