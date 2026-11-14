# Validate a Trajectory Against Derivative Limits

## Intuition

Limits are meaningful only when derivative order and units stay aligned. Reporting which derivative exceeded its envelope is more useful than one unexplained failure bit.

## Mathematics and conventions

Let $x^{(k)}_{nd}$ be the sampled derivative of order $k\in\{1,2,3\}$ for sample $n$ and joint $d$, and $L_{kd}>0$ its bound in rad/s to that order.

$$V_{ndk}=\mathbf1[|x^{(k)}_{nd}|>L_{kd}],\qquad R_{kd}=\max_n |x^{(k)}_{nd}|/L_{kd}.$$

$V$ has shape $N\times D\times3$ and $R$ shape $3\times D$. Ratios are dimensionless. Empty evidence is assigned zero ratios for storage convenience but a failing overall verdict.

## Visual computation trace

| Derivative | Sample | Bound | Ratio |
| --- | --- | --- | --- |
| Velocity | 2.2 rad/s | 2 rad/s | 1.1 |
| Acceleration | -3 rad/s² | 3 rad/s² | 1 |
| Jerk | 4 rad/s³ | 4 rad/s³ | 1 |

## Worked examples

1. One joint sample with velocity `2`, acceleration `-3`, jerk `4`, limits `[[2.],[3.],[4.]]` yields violations `[[[False,False,False]]]`, max ratios `[[1.],[1.],[1.]]`, passed True.
2. Change velocity to `2.2`: only its velocity flag is True, maximum velocity ratio is `1.1`, and passed is False.

## Why this matters on a robot

A sparse log can miss a peak between samples. Use this report to diagnose measured or analytically sampled states, then separately validate continuous segment extrema and robot dynamics.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2105.04830). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
