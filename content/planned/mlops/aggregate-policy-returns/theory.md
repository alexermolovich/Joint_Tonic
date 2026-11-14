# Aggregate Mean and Worst-Case Policy Returns

## Intuition

Two policies can have the same average return while one fails badly in a small region of randomized dynamics. Keep the typical result, the single worst episode, and a lower-tail average side by side.

## Fractional empirical tail

Let R in R^(P×E) contain dimensionless returns. Policy p has mean and worst case

$$\mu_p=\frac1E\sum_e R_{pe},\qquad w_p=\min_eR_{pe}.$$

Sort its episode returns into x_0<=...<=x_(E-1). For tail fraction alpha, define q=alpha E, k=floor(q), a=q-k. Average exactly q units of empirical probability mass:

$$T_p=\frac{\sum_{i=0}^{k-1}x_i+a x_k}{q}.$$

Omit the final term when k=E. Fractional weighting avoids a discontinuous ceil-based sample count. At alpha=1 this equals the overall mean; at q<1 it equals the minimum.

## Visual tail trace and worked example

| Sorted return | Included mass at alpha=0.375,E=4 |
|---|---|
| 0 | 1 |
| 2 | 0.5 |
| 4 | 0 |
| 6 | 0 |

q=1.5, so tail=(0+0.5*2)/1.5=2/3, mean3, worst0. The table is the static visual and text alternative.

## Why this matters on a robot

A policy brittle to high latency can look excellent on nominal dynamics. Episode distributions and reward scales must match across policies: averaging metres with success bonuses from a different reward design is meaningless. Small E makes tail estimates unstable; this task does not quantify that uncertainty.

Prerequisite: [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions).

## Source and scope

This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.
