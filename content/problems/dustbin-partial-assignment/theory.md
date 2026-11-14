# Reject Unmatched Features with Dustbins

## Intuition

A feature that disappears between images should not be forced onto an unrelated point. Dustbins add destinations for missing correspondences while preserving the mass accounting needed by partial assignment.

## Mathematics and conventions

For N source and M target features, augment $S\in\mathbb R^{N\times M}$ with a scalar bin logit $\alpha$ to form $\bar S\in\mathbb R^{(N+1)\times(M+1)}$. The normalized marginals are

$$a=\frac{[\underbrace{1,\ldots,1}_{N},M]}{N+M},\qquad b=\frac{[\underbrace{1,\ldots,1}_{M},N]}{N+M}.$$

Thus the source-side bin can absorb all M target features, and the target-side bin all N source features. Apply log-Sinkhorn to obtain unit-total transport P, then rescale $A=(N+M)P$. Real-feature rows and columns target mass 1; bin capacities differ for rectangular sets. Row i is dustbin-dominant exactly when

$$A_{i,M}>\max_{j<M}A_{ij}.$$

All values are dimensionless. This inequality is a declared operational diagnostic. Mutual confidence extraction is a separate component and does not silently apply it.

## Visual computation trace

| N=1,M=1, all logits0 | Real target | Dustbin target | Row total |
| --- | --- | --- | --- |
| Real source | .5 | .5 | 1 |
| Dustbin source | .5 | .5 | 1 |
| Tie decision | real feature retained as possible | not dominant | |

## Worked examples

1. One source and one target feature, real score 0 and dustbin score 0: every entry of the `2x2` assignment is 0.5. Both unmatched flags are False because the real and dustbin values tie.
2. One source and one target, real score -2 and dustbin score 0, 100 iterations: real-real and dustbin-corner values approach `1/(1+e)`; the two off-diagonal values approach `e/(1+e)`. Both feature unmatched flags are True.

## Why this matters on a robot

Images need not contain the same number of visible keypoints. Uniform bin capacity would distort rectangular assignments. Even a non-dustbin result still needs mutual consistency and downstream geometry.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1911.11763). [log-sinkhorn-assignments](/problems/log-sinkhorn-assignments)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
