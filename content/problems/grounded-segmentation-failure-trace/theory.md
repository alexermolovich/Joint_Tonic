# Build a Grounded Segmentation Pipeline and Trace Failures

## Intuition

Grounding, mask quality and usable geometry are distinct stages. A failure trace identifies the earliest broken contract instead of flattening every rejected query into “no object.”

## Math and staged decisions

For query $q$, phrase scores $s_{qp}$ and quality $a_q$ are dimensionless. Let $p_q$ be the lowest-index maximum-score phrase. Its boolean mask $M_q\in\{0,1\}^{H\times W}$ has area
$$A_q=\sum_{y,x}M_{qyx}.$$
After passing phrase and quality thresholds and requiring $A_q>0$, compute a pixel-center centroid:
$$\bar u_q=A_q^{-1}\sum_{y,x}M_{qyx}(x+0.5),\qquad \bar v_q=A_q^{-1}\sum_{y,x}M_{qyx}(y+0.5).$$
Row index y increases down; column x increases right. Centroids are pixels, not 3D grasp positions.

| Stage | Condition | First failure |
|---|---|---|
| Grounding | max phrase score ≥ threshold | low_grounding |
| Mask ranking | predicted quality ≥ threshold | low_mask_quality |
| Geometry | positive foreground area | empty_mask |
| Output | preserve query identity | accepted |

For foreground centers (0.5,0.5),(1.5,0.5), area is2 and centroid is(1,0.5). A high-quality but wrong-object mask may pass these checks; semantic correctness still requires evaluation.

## Why this matters on a robot

A failure trace separates perception stages for debugging and prevents division by zero for empty masks. Query identity must survive filtering so language labels and masks stay aligned. This original interface composes Grounding-DINO-like scores and SAM-like masks without claiming to implement either neural network or determine safe graspability.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2303.05499). [grounding-phrase-box-decoding](/problems/grounding-phrase-box-decoding) · [sam-mask-ranking](/problems/sam-mask-ranking)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
