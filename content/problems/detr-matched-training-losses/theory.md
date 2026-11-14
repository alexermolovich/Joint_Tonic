# Compute DETR Classification, L1, and GIoU Losses

## Intuition

Matching chooses which prediction explains each target. Training then supervises all query classes, but geometry only for matched queries. Unmatched queries learn no-object with reduced weight.

## Math and reduction rules

For $Q$ queries and $C$ real classes, target class $y_q\in\{0,\ldots,C\}$ is C for unmatched queries. Let $w_q=\alpha$ for no-object and1 otherwise, where $\alpha$ is eos_weight.
$$L_{\mathrm{class}}=\frac{\sum_q w_q[-\log\operatorname{softmax}(z_q)_{y_q}]}{\sum_q w_q}.$$
For $M$ targets with injective assignment $\sigma$,
$$L_1=\frac{\sum_j\|\hat b_{\sigma(j)}-b_j\|_1}{\max(M,1)},\quad L_G=\frac{\sum_j[1-\operatorname{GIoU}(\hat b_{\sigma(j)},b_j)]}{\max(M,1)}.$$
Center-size boxes are dimensionless image fractions. After converting to unclipped corners, GIoU is $I/U-(E-U)/E$, where I is intersection area,U union and E smallest enclosing rectangle area. Total is $L_{\mathrm{class}}+5L_1+2L_G$.

| Prediction subset | Class supervision | Geometry supervision |
|---|---|---|
| Matched query | target real class,weight1 | center-size L1 + paired GIoU |
| Unmatched query | no-object,weight α | none |
| Empty target image | all no-object | zero geometric losses |

Touching half-image boxes have union=enclosure=1 and intersection0,so GIoU0. Their centers differ by0.5 in x, giving L1=0.5 and total ln2+4.5 for zero logits. Matching cost uses negative probability; this training loss uses negative log probability and must not be substituted with the former.

## Why this matters on a robot

Incorrect no-object weighting can drown out rare objects. Averaging box error over all queries dilutes supervision when object counts are small. This single-image component preserves the reduction semantics while omitting auxiliary layers and distributed normalization of full DETR training.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2005.12872). [detr-hungarian-assignment](/problems/detr-hungarian-assignment) · [detr-matching-cost](/problems/detr-matching-cost)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
