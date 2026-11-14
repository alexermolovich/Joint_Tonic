# Combine Competing Task-Space Accelerations

## Intuition

Each metric says which directions a policy cares about. Add the metric-weighted requests, then solve only in directions supported by the combined metric; averaging raw accelerations ignores that information.

## Mathematics and conventions

For $K$ policies in a common $D$-dimensional space, metric $M_k\succeq0$ and desired acceleration $a_k\in\mathbb R^D$ define

$$M=\sum_kM_k,\qquad f=\sum_kM_ka_k,\qquad a=M^\dagger f.$$

With symmetric eigendecomposition $M=V\operatorname{diag}(\lambda)V^T$, the contract uses

$$a=\sum_{i:\lambda_i>10^{-10}\lambda_{max}}v_i\frac{v_i^Tf}{\lambda_i}.$$

No direction is retained when M is zero. Metrics are dimensionless and accelerations/natural forces have units 1/s². The cutoff deliberately discards relatively weak directions; it is a stated numerical choice rather than a hidden damping term.

## Visual computation trace

| Policy | Metric weight | Desired acceleration | Natural force |
| --- | --- | --- | --- |
| A | 1 | 2 | 2 |
| B | 3 | -2 | -6 |
| Combined | 4 | -1 after resolve | -4 |

## Worked examples

1. Two scalar metrics `[[[1.]],[[3.]]]` and accelerations `[[2.],[-2.]]` yield metric `[[4.]]`, force `[-4.]`, acceleration `[-1.]`, rank `1`.
2. One metric `diag([1.,0.])` and acceleration `[[2.,9.]]` yield force `[2.,0.]`, resolved acceleration `[2.,0.]`, rank `1`. The unweighted direction is set to zero.

## Why this matters on a robot

A nearly unsupported direction can amplify numerical noise if inverted without a rank policy. This bounded resolve does not make conflicting leaf policies globally collision-free or dynamically stable.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1811.07049). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
