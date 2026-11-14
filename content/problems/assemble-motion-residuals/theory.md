# Assemble Obstacle and Prior Residuals

## Intuition

A nonlinear least-squares solver expects comparable residual scales. The prior is already whitened; only the clearance hinge needs scaling before the two pieces can be concatenated.

## Mathematics and conventions

Let $p\in\mathbb R^P$ be a whitened prior, $d_i$ a signed clearance, $\epsilon\ge0$ a clearance margin, and $\sigma>0$ an obstacle standard-deviation scale. Distances, margin and scale are meters.

$$h_i=\frac{\max(0,\epsilon-d_i)}{\sigma},\quad r=\begin{bmatrix}p\\h\end{bmatrix},\quad E=\tfrac12p^Tp+\tfrac12h^Th.$$

Both residual blocks and $E$ are dimensionless. This factor penalizes clearance below the margin, including separated surfaces near an obstacle. The chosen isotropic obstacle covariance is $\sigma^2I$; no independent prior scaling is applied again.

## Visual computation trace

| Input | Hinge in meters | Whitened residual |
| --- | --- | --- |
| Clearance 0.1, margin 0.3 | 0.2 | 1 with sigma 0.2 |
| Clearance 0.5, margin 0.3 | 0 | 0 |
| Prior residual | already scaled | 2 |

## Worked examples

1. Prior `[2.]`, clearances `[0.1,0.5]`, margin `0.3`, sigma `0.2` give residual `[2.,1.,0.]`, prior cost `2`, obstacle cost `0.5`, total `2.5`.
2. Empty prior, clearance `[-0.1]`, margin `0`, sigma `0.1` give residual `[1.]` and total cost `0.5`.

## Why this matters on a robot

A zero obstacle residual means only the supplied sample clears the chosen margin. It does not check the path between samples; scaling the prior twice can also distort the smoothness/collision tradeoff.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1707.07383). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
