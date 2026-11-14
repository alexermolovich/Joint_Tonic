# Compute an Entropy-Regularized State Value

## Intuition

A stochastic robot policy values both task reward and action entropy. Estimate its soft state value from sampled actions, while keeping the number of usable samples visible instead of interpreting an empty row as strong evidence.

## Mathematical mechanism

For sampled action k at state b, $Q_{bk}$ is its value and $\ell_{bk}$ its log density. With Boolean validity M and entropy coefficient alpha, $$V_b=\frac{\sum_k M_{bk}(Q_{bk}-\alpha\ell_{bk})}{\sum_k M_{bk}}.$$ Define V as zero when its sample count vanishes. Alpha converts natural-log entropy to the reward scale. This is a Monte Carlo estimate, not an exact integration over all actions.

## Visual computation trace

| Sample | Q | log density | alpha | Soft value |
|---|---|---|---|---|
| 0 | 2 | -1 | 0.5 | 2.5 |
| 1 | 4 | -2 | 0.5 | 5 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Q=[[2,4]], log probabilities=[[-1,-2]], both valid, alpha=.5 returns values[3.75], counts[2].

## Why this matters on a robot

A robot learning pipeline depends on correct action likelihoods, terminal flags and dataset identity. A numerically small loss cannot repair incorrect replay semantics or absent action coverage.

## Physical contract and limits

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

Source: [primary paper](https://arxiv.org/abs/1801.01290). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
