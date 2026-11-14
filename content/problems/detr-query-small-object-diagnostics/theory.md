# Diagnose Query Collapse and Missed Small Objects

## Intuition

Redundant query representations and missing small objects can coexist, but they are different symptoms. Inspect feature similarity and target coverage separately before changing the model.

## Math and diagnostic split

Query feature $f_i\in\mathbb R^D$ is normalized to $u_i=f_i/\|f_i\|_2$. Potentially redundant pairs satisfy $i<j$ and $u_i^\top u_j\ge\tau_c$. For target box $b_m$ with normalized area $A_m$, small-object miss is
$$\mathrm{miss}_m=\mathbf1[A_m\le A_{\max}]\land\neg\bigvee_q[\operatorname{IoU}(\hat b_q,b_m)\ge\tau_I].$$
IoU is intersection area divided by union area. Areas and thresholds are dimensionless image fractions; this coverage test does not check class identity or enforce unique assignment.

| Branch | Input | Output evidence |
|---|---|---|
| Query redundancy | Q × D features | lexicographic similar pairs |
| Small-object slice | M box areas | target indices under area cutoff |
| Localization coverage | Q × M IoU | whether any query covers each target |

Two parallel vectors [1,0] and[2,0] have cosine1 regardless of magnitude. If both boxes occupy the image origin, they cover the origin target but cannot cover a far-corner target. Similarity alone cannot say why the second target was missed.

## Why this matters on a robot

Small handles and tools may matter more than large easy objects. Overall detection metrics can hide their failure. High query similarity is only a warning: model-layer choice and feature scaling influence it. Combine these original diagnostic summaries with class-aware evaluation and visual inspection.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2005.12872). [box-iou-broadcast](/problems/box-iou-broadcast)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
