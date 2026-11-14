# Sample Hierarchical Depth Intervals

## Intuition

Coarse rendering weights tell a fine sampler where useful mass lies along a ray. Inverse-CDF sampling converts supplied quantiles into depths. The small mass floor keeps every interval reachable without needing a random generator inside the task.

## Mathematics and physical meaning

For one ray, edges $e_0<\cdots<e_S$ are metric depths in meters and $w_i\ge0$ are dimensionless interval masses. They are not density per meter. Define
$$p_i=\frac{w_i+10^{-5}}{\sum_j(w_j+10^{-5})},\quad F_0=0,\quad F_{i+1}=F_i+p_i.$$
Set the final CDF value exactly to 1 to remove accumulated rounding. For quantile $u\in[0,1]$, choose $i$ with right-sided search in $F$, minus one and clipped to $[0,S-1]$. Then
$$t=e_i+\frac{u-F_i}{F_{i+1}-F_i}(e_{i+1}-e_i).$$
Input arrays have shapes edges $(B,S+1)$, weights $(B,S)$ and quantiles $(B,K)$; output depths are $(B,K)$ in the original quantile order. Endpoints $u=0,1$ give the near/far edge. Equal zero weights make intervals equally probable, not depth uniformly distributed when widths differ.

## Visual trace

| Quantile | Interval for edges `[0,1,3]` | Depth with equal masses |
|---:|---|---:|
| 0 | first | 0 |
| .25 | first | .5 |
| .5 | second | 1 |
| .75 | second | 2 |
| 1 | second | 3 |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** Edges `[[0, 1, 3]]`, weights `[[0, 0]]` and quantiles `[[0,.25,.5,.75, 1]]` produce depths `[[0,.5, 1, 2, 3]]`.

**Example 2.** A single interval with edges `[[2, 6]]`, weight `[[5]]` and quantiles `[[.75,.25]]` produces `[[5, 3]]`, preserving the unsorted query order.

## Why this matters on a robot

A neural scene model can spend more field queries near visible surfaces. Multiplying supplied masses by interval widths again biases the sampling distribution. This component does not evaluate a field, train NeRF or certify obstacle occupancy.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2003.08934). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
