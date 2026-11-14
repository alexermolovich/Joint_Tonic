# Build Advantage-Weighted Action Weights

## Intuition

Offline policy fitting can prefer logged actions that look better than the state-value baseline. Exponential advantage weights make that preference explicit, while a declared cap keeps one high estimate from dominating the supervised update.

## Mathematical mechanism

Every input tensor in the equation has shape (B,T): B is the number of independent streams and T the number of samples. $M_{bt}$ is the Boolean validity mask; masked entries contribute zero.

For advantage $A=Q_{target}-V$ and inverse reward scale beta, $$w=M\exp(\min(\beta A,\log w_{max})).$$ This is an unnormalized supervised weight; dividing by the batch sum would change its contract. Beta A must be dimensionless. Capping before exp prevents numerical overflow even when Q-V is large.

## Visual computation trace

| Advantage | beta | Cap | Weight |
|---|---|---|---|
| 0 | 1 | 2 | 1 |
| 1 | 1 | 2 | 2 |
| 100 | 1 | 2 | 2 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Q=[[0,1,100]], V=zeros, all valid, beta1,max_weight2 returns[[1,2,2]].

## Why this matters on a robot

A robot learning pipeline depends on correct action likelihoods, terminal flags and dataset identity. A numerically small loss cannot repair incorrect replay semantics or absent action coverage.

## Physical contract and limits

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

Source: [primary paper](https://arxiv.org/abs/2110.06169). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
