# Compare Validation Loss with Rollout Success

## Intuition

Validation loss asks how predictions match a fixed demonstration set. Rollout success asks what happens after the policy changes the next observation. Those questions can disagree. This component makes that disagreement visible without pretending that a small success count is certain.

## Two rankings, two objectives

For checkpoint i, let $\ell_i$ be its supplied validation loss, $s_i$ its successful rollouts and $n_i>0$ its trial count. Observed success is

$$
\hat p_i=\frac{s_i}{n_i}.
$$

Loss is dimensionless under a shared upstream definition; success and count are dimensionless. Lower loss is preferred for the offline order; higher success fraction is preferred for the rollout order. Compare fractions using integer cross-products:

$$
\hat p_i>\hat p_j\quad\Longleftrightarrow\quad s_i n_j>s_j n_i.
$$

No floating-point division is needed to choose the order. IDs supply the declared final tiebreak.

## Visual: the winners disagree

| Checkpoint | Loss | Successful / total rollouts | Success | Offline rank | Rollout rank |
|---|---:|---|---:|---:|---:|
| early | 0.1 | 1/10 | 0.1 | 1 | 2 |
| later | 0.2 | 8/10 | 0.8 | 2 | 1 |

The two first IDs differ, so disagree is true. This static comparison is the visual and its text alternative.

## What the result does not establish

Observed rates from different trial counts have different uncertainty. This task orders the supplied evidence exactly; a follow-on selection policy should require coverage and independent evaluation. It must not tune repeatedly on a purported final test set.

## Why this matters on a robot

Small prediction errors can move the gripper into states absent from demonstrations, causing compounding failures. A policy with slightly higher supervised error may recover better in closed-loop behavior. Equally, one lucky rollout does not establish robust performance.

## Questions

1. Why compare success fractions instead of successful-trial counts?
2. Can disagree=False prove the offline objective is a reliable model-selection criterion?

## Sources and prerequisites

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. [Primary source](https://arxiv.org/abs/2108.03298), Offline demonstration evaluation and stopping criteria. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

