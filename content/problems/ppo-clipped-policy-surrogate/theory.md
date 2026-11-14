# Compute the Clipped Policy Surrogate

## Intuition

PPO compares the new policy with the policy that collected each action. The clipped objective limits an overly optimistic improvement, and the sign of the advantage determines which probability change should be limited.

## Mathematical mechanism

Let $\ell_{bt}=\log\pi_{new}-\log\pi_{old}$ and $r_{bt}=\exp(\ell_{bt})$. Advantage $A_{bt}$ is a supplied reward-unit estimate. With Boolean validity M and clip width epsilon, $$z_{bt}=M_{bt}\min(r_{bt}A_{bt},\operatorname{clip}(r_{bt},1-\epsilon,1+\epsilon)A_{bt}),\qquad L=-\frac{\sum z_{bt}}{\sum M_{bt}}.$$ Set L to zero when there is no valid sample. The minimum acts on the signed products, so clipping the ratio first and using only that branch is incorrect.

## Visual computation trace

| Advantage | Ratio | Raw term | Clipped term | Minimum |
|---|---|---|---|---|
| +1 | 1.5 | 1.5 | 1.2 | 1.2 |
| -1 | 1.5 | -1.5 | -1.2 | -1.5 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Positive advantage1 ratio1.5 epsilon.2 clips objective to1.2; negative advantage-1 ratio1.5 gives-1.5, not-1.2.

## Why this matters on a robot

A robot action with negative advantage should become less likely. Using the wrong clipping branch can reward probability increases for that action. Frozen old log densities must come from the actual behavior policy; stale or recomputed likelihoods change the objective.

## Physical contract and limits

Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units. Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits. Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.

Source: [primary paper](https://arxiv.org/abs/1707.06347). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
