# Normalize Exponential Trajectory Cost Weights

## Intuition

Low-cost rollouts contribute more to the next controller update. Subtracting the best valid cost keeps the largest exponential at one, so extreme absolute costs do not overflow.

## Mathematics and conventions

For valid rollout set $\mathcal V$, corrected costs $S_k$ and positive temperature $\lambda$ in matching cost units,

$$w_k=\frac{\exp(-(S_k-S_{min})/\lambda)}{\sum_{j\in\mathcal V}\exp(-(S_j-S_{min})/\lambda)},\qquad N_{eff}=1/\sum_k w_k^2.$$

Invalid indices receive zero weight. Weights and effective sample count are dimensionless. $N_{eff}$ equals the valid sample count for uniform weights and approaches one when one sample dominates. This diagnostic is not a confidence interval or a claim of independent effective trajectories.

## Visual computation trace

| Rollout cost | Unnormalized value | Normalized weight |
| --- | --- | --- |
| 0 | 1 | 0.75 |
| log(3) | 1/3 | 0.25 |

## Worked examples

1. Costs `[0.,log(3)]`, both valid, temperature1 gives weights `[0.75,0.25]`, effective samples `1.6`, best index0.
2. Costs `[2.,-100.,2.]`, validity `[True,False,True]`, temperature1 gives weights `[0.5,0.,0.5]`, effective samples2, best index0.

## Why this matters on a robot

Weight collapse can make a controller depend on one lucky simulated rollout. Increasing sample count without fixing dynamics or temperature may leave that failure unchanged; inspect effective sample count alongside control quality.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1509.01149). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
