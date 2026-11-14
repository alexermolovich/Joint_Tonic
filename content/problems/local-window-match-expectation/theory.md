# Refine a Match in a Local Window

## Intuition

A hard argmax can move abruptly between neighboring cells. A local probability-weighted position produces a subpixel estimate, while its covariance shows whether probability is concentrated or spread across the window.

## Mathematics and conventions

For query $q_b\in\mathbb R^D$ and window descriptor $w_{bij}\in\mathbb R^D$, define dimensionless logits and probabilities

$$\ell_{bij}=q_b^\top w_{bij}/\sqrt D,\qquad p_{bij}=\frac{e^{\ell_{bij}}}{\sum_{u,v}e^{\ell_{buv}}}.$$

Let cell displacement in pixels be $g_{ij}=((j-c)s_x,(i-c)s_y)$, where $c=\lfloor S/2\rfloor$ and $s_x,s_y$ are pixels per cell. Then

$$\mu_b=\sum_{i,j}p_{bij}g_{ij},\qquad \Sigma_b=\sum_{i,j}p_{bij}(g_{ij}-\mu_b)(g_{ij}-\mu_b)^\top.$$

Mu has shape $(2,)$ and pixel units; Sigma has shape $(2,2)$ and square-pixel units. Add mu to the supplied coarse target center. Off-diagonal terms describe correlated horizontal/vertical uncertainty. This population moment diagnostic is distinct from a trained confidence calibration or the paper's specific normalized uncertainty output.

## Visual computation trace

| Uniform 3x3 window | x offset | y offset |
| --- | --- | --- |
| Possible cell values | -1,0,1 equally | -1,0,1 equally |
| Mean | 0 | 0 |
| Unit-scale variance | (1+0+1)/3=2/3 | 2/3 |
| Pixel scales2,3 | variance8/3 | variance6 |

## Worked examples

1. Zero query/window descriptors with S=3 yield uniform probability 1/9. With pixel_scale `[1.,1.]`, the offset is `[0.,0.]` and covariance `[[2/3,0],[0,2/3]]`. Scale `[2.,3.]` changes it to `[[8/3,0],[0,6]]`.
2. D=1, query 1, a `3x3` window with center value log(8) and all others zero gives center probability 1/2 and every other cell 1/16. Its offset is zero and covariance is `[[0.375,0],[0,0.375]]` at unit scale.

## Why this matters on a robot

An expectation between two peaks can lie on a location with little evidence. Covariance exposes dispersion but does not prove geometric correctness; the refined correspondence still needs image-pair geometry checks.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2104.00680). [dual-softmax-coarse-matches](/problems/dual-softmax-coarse-matches)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
