# Resize the spatial grid without moving the class token

## Intuition

Changing image resolution changes the number of patch positions. A learned position table is not simply a list to stretch: its patch rows represent a2D grid, while its first class-token row has a different role.

## Separate sequence and space

Let $P\in\mathbb R^{1\times(1+H_0W_0)\times D}$ contain D-channel position embeddings. Keep $P_{\mathrm{cls}}=P[:,0:1,:]$. Reshape the remaining rows to $G\in\mathbb R^{1\times D\times H_0\times W_0}$ and resize spatially:

$$
G'=\operatorname{Bicubic}_{H_1,W_1}(G),\qquad
P'=[P_{\mathrm{cls}};\operatorname{flatten}_{\mathrm{row-major}}(G')].
$$

The output has shape $(1,1+H_1W_1,D)$. Channel coordinates are learned and dimensionless; they are not image intensities or physical positions.

## Visual: class row stays outside the grid

| Portion | Before | Operation | After |
|---|---|---|---|
| Class position | 99 | Copy unchanged | 99 |
| Spatial positions | [[1,2],[3,4]] | Bicubic2x2→1x1 | [[2.5]] |
| Sequence | [99,1,2,3,4] | Rejoin | [99,2.5] |

This static layout trace is the text alternative. Mixing the class row into spatial interpolation would give the wrong topology.

## Coordinate convention

With align_corners=false, target column j maps to source coordinate

$$
x_{\mathrm{src}}=(j+\tfrac12)\frac{W_0}{W_1}-\tfrac12,
$$

and the analogous expression applies to rows. Bicubic interpolation uses nearby samples and can overshoot their range. Do not clip output embeddings. The pinned PyTorch operator, antialias=false and this coordinate convention define the exact numerical contract; the paper's general interpolation idea alone does not determine every library option.

## Why this matters on a robot

A higher camera resolution can improve small-object evidence while changing the transformer input geometry. A checkpoint's interpolation settings must travel with deployment preprocessing. Resizing the sequence as1D or assuming a square grid silently scrambles rectangular camera layouts.

## Questions and source

Why preserve the class row exactly? It has no spatial pixel-grid coordinate. Why keep gradients? Fine-tuning may update the original position parameters through the resized table.

Source: [ViT resolution transfer](https://arxiv.org/abs/2010.11929). First implement [token assembly](/problems/vit-patch-class-tokens). This task resizes position parameters, not images or full checkpoints.
