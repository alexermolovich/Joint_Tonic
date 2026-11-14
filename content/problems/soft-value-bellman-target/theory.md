# Compute an Entropy-Regularized Bellman Target

## Intuition

One-step critic targets combine immediate reward with a value estimate of the next physical state. True task termination removes the future term; an administrative rollout limit does not necessarily end the task.

## Mathematical mechanism

Every input tensor in the equation has shape (B,T): B is the number of independent streams and T the number of samples. $M_{bt}$ is the Boolean validity mask; masked entries contribute zero.

For reward r, next-state value V, true-terminal flag d and discount gamma, $$y_{bt}=M_{bt}\left(r_{bt}+\gamma(1-d_{bt})V_{bt}^{next}\right).$$ B indexes streams and T aligned transitions. SAC supplies a soft value that already includes entropy; IQL supplies an expectile value. The shared arithmetic does not make those learned value functions interchangeable.

## Visual computation trace

| Record | reward | next value | terminal | target at gamma0.5 |
|---|---|---|---|---|
| ongoing | 1 | 4 | false | 3 |
| task ended | 1 | 4 | true | 1 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

rewards=[[1,1]], next_values=[[4,4]], terminated=[[False,True]], both valid, gamma=.5 returns [[3,1]].

## Why this matters on a robot

A robot learning pipeline depends on correct action likelihoods, terminal flags and dataset identity. A numerically small loss cannot repair incorrect replay semantics or absent action coverage.

## Physical contract and limits

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

Source: [primary paper](https://arxiv.org/abs/1801.01290). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
