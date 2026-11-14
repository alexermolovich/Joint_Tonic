# Compute a Conservative Q Penalty

## Intuition

Conservative Q-learning compares values across the entire finite action set against values of actions that actually appear in the dataset. The gradient raises logged-action support relative to the soft maximum over alternatives.

## Mathematical mechanism

For $Q\in\mathbb R^{B\times A}$ and K logged indices $a_{bk}$, define $$c_b=\log\sum_{a=1}^{A}e^{Q_{ba}}-\frac1K\sum_{k=1}^KQ_{b,a_{bk}},\quad L=\frac{\alpha}{N}\sum_b M_b c_b.$$ M is the Boolean row-validity mask, N its true count, and alpha the nonnegative penalty coefficient. With empirical logged frequency f, the gradient is $\alpha M_b(\operatorname{softmax}(Q_b)-f_b)/N$. Duplicate logged indices contribute repeatedly. Empty valid support gives zero loss and gradient. Subtract the row maximum inside log-sum-exp. Q is expressed in the fixed dimensionless reward convention used by this finite-action teaching objective.

## Visual computation trace

| Action | Q | Softmax | Logged frequency | Gradient at alpha=1 |
|---|---|---|---|---|
| 0 | 0 | 0.5 | 1 | -0.5 |
| 1 | 0 | 0.5 | 0 | 0.5 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

With Q = [[0, 0]], logged indices = [[0]], valid = [True] and alpha = 1, the loss and raw penalty are log(2), and the gradient is [[-0.5, 0.5]].

## Why this matters on a robot

Incorrect replay support or inconsistent visual views can teach a robot critic to trust actions that its training data cannot justify. These diagnostics do not establish physical safety.

## Physical contract and limits

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

Source: [primary paper](https://arxiv.org/abs/2006.04779). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
