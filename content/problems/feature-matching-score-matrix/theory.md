# Build a Feature-Matching Score Matrix

## Intuition

A matching score compares feature-channel evidence across images. The channel scaling is part of the contract; silently converting to cosine similarity changes both magnitude and downstream confidence.

## Mathematics and conventions

Let source descriptors be $A\in\mathbb R^{N\times D}$ and target descriptors $B\in\mathbb R^{M\times D}$. For source point i and target point j,

$$S_{ij}=\frac{1}{\sqrt D}\sum_{c=1}^{D}A_{ic}B_{jc},\qquad S=AB^\top/\sqrt D.$$

The score matrix has shape $(N,M)$ and dimensionless units. Each row corresponds to one source keypoint; each column to one target keypoint. There is no probability normalization yet. Source and target point counts may differ, and descriptor magnitudes carry information rather than being discarded by row normalization.

## Visual computation trace

| Source descriptor | Target descriptor | Dot product | D | Score |
| --- | --- | --- | --- | --- |
| [2] | [4] | 8 | 1 | 8 |
| [1,1,1,1] | same | 4 | 4 | 2 |

## Worked examples

1. With D=1, source `[[2.],[3.]]` and target `[[4.]]` give scores `[[8.],[12.]]`.
2. With D=4 and both sets containing one descriptor `[1.,1.,1.,1.]`, the dot product 4 is divided by sqrt(4), giving `[[2.]]`. Cosine similarity would incorrectly give 1.

## Why this matters on a robot

Strong descriptor agreement can still come from repeated texture. The score matrix needs assignment and geometric checks before its entries become camera-motion constraints.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1911.11763). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
