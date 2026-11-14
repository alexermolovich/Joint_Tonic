# Apply Tanh Action Log-Probability Correction

## Intuition

Squashing a Gaussian sample into an action interval changes its probability density. Correcting the Jacobian keeps the actor likelihood consistent with the bounded actions actually given to the critic.

## Mathematical mechanism

For unsquashed $u\in\mathbb R^D$ and positive scales s, $a_j=s_j\tanh(u_j)$. The transformed density is $$\log\pi(a)=\log p(u)-\sum_j[\log s_j+2(\log2-u_j-\operatorname{softplus}(-2u_j))].$$ The bracket is the log absolute Jacobian determinant per channel. Use softplus(x)=logaddexp(0,x), because direct log(1-tanh(u)^2) loses precision for large magnitudes.

## Visual computation trace

| u | scale | action | log Jacobian |
|---|---|---|---|
| 0 | 2 | 0 | log2 |
| 0 | 3 | 0 | log3 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

u=[[0,0]], base=[-2], scale=[2,3] returns zero actions and log_prob[-2-log(6)].

## Why this matters on a robot

A robot learning pipeline depends on correct action likelihoods, terminal flags and dataset identity. A numerically small loss cannot repair incorrect replay semantics or absent action coverage.

## Physical contract and limits

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

Source: [primary paper](https://arxiv.org/abs/1801.01290). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
