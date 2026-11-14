# Report Performance by Demonstration Quality

## Intuition

Demonstration quality is one axis of an experiment, and task difficulty is another. Pooling every rollout into one number lets a heavily sampled easy task dominate. Retain task slices first, then make the aggregation rule visible.

## Count trials before averaging

For quality q and task t, let $n_{qt}$ count trials and $s_{qt}$ count successes. A recorded trial contributes one count even when its tuple matches another trial. Define

$$
\hat p_{qt}=\frac{s_{qt}}{n_{qt}},\qquad
\hat p_q^{\mathrm{pool}}=\frac{\sum_t s_{qt}}{\sum_t n_{qt}},\qquad
\hat p_q^{\mathrm{macro}}=\frac{1}{|T_q|}\sum_{t\in T_q}\hat p_{qt}.
$$

$T_q$ is the set of observed tasks for quality q. All rates are dimensionless; counts are numbers of rollouts. There is no invented rate for an unobserved task.

## Visual: aggregation changes the question

| Task under expert condition | Trials | Successes | Task rate | Pooled weight | Macro weight |
|---|---:|---:|---:|---:|---:|
| easy | 9 | 9 | 1 | 0.9 | 0.5 |
| hard | 1 | 0 | 0 | 0.1 | 0.5 |

The pooled answer0.9 describes the sampled trial mixture. The macro answer0.5 gives both observed tasks equal influence. The table is the static visual and text alternative.

## Coverage remains part of the evidence

Two quality conditions can cover different tasks. Their macro rates are then averages over different sets, so a direct causal ranking is not justified by this function. Keep by_slice output alongside any aggregate.

## Why this matters on a robot

A demonstration set may look excellent on routine grasps while missing recovery behavior in clutter. Reporting only a pooled percentage can hide a weak operational slice. Quality labels also need traceable definitions; the algorithm cannot infer demonstrator expertise from outcome counts.

## Questions

1. Why should identical outcome tuples not be deduplicated?
2. Why is an absent task different from a task with zero successes?

## Sources and prerequisites

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. [Primary source](https://arxiv.org/abs/2108.03298), Offline demonstration evaluation and stopping criteria. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

