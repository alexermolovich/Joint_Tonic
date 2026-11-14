# Average Augmented Bellman Targets

## Intuition

Several augmentations of one next observation estimate the same transition value. Average those estimates before bootstrapping, while keeping true termination separate from missing imagery.

## Mathematical mechanism

For next-state view values $V\in\mathbb R^{B\times K}$ and Boolean mask M, $$\bar V_b=\frac{\sum_k M_{bk}V_{bk}}{n_b},\qquad y_b=r_b+\gamma(1-d_b)\bar V_b.$$ Here n is the valid-view count, d true termination, gamma the discount, and r the one reward for this transition. A terminal with n=0 returns y=r directly, not an arithmetic product with NaN. A nonterminal with no views is invalid. Values are already soft values when entropy is required.

## Visual computation trace

| Transition | View values | Mean | Target at gamma 0.5 |
|---|---|---|---|
| ongoing, reward 1 | 2, 4 | 3 | 2.5 |
| terminal, reward 1 | absent | unknown | 1 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Reward [1], next values [[2, 4]], both views valid, terminated = [False] and gamma = 0.5 yield mean_next = [3], counts = [2] and targets = [2.5].

## Why this matters on a robot

Incorrect replay support or inconsistent visual views can teach a robot critic to trust actions that its training data cannot justify. These diagnostics do not establish physical safety.

## Physical contract and limits

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

Source: [primary paper](https://arxiv.org/abs/2004.13649). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
