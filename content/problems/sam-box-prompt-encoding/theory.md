# Encode a Box Prompt with Positional Features

## Intuition

A box supplies two spatial constraints. Separate corner types prevent the prompt encoder from treating the box as two interchangeable positive points.

## Math and corner trace

For box $b_i=(x_1,y_1,x_2,y_2)$ in pixel-index coordinates, let $p_{i0}=(x_1,y_1)$ and $p_{i1}=(x_2,y_2)$. Image dimensions $(H,W)$ are pixels; $B\in\mathbb R^{2\times F}$ and corner vectors $E\in\mathbb R^{2\times2F}$ are supplied.
$$q_{ik}=2(p_{ik}+0.5)/[W,H]-1,\quad \theta_{ik}=2\pi q_{ik}B,\quad z_{ik}=[\sin\theta_{ik};\cos\theta_{ik}]+E_k.$$
The output shape is $N\times2\times2F$: the middle axis is corner identity, and the last axis is a dimensionless embedding.

| Corner | x in 2-pixel image | Normalized x | Phase with frequency 0.5 | Sine |
|---|---|---|---|---|
| top-left | 0 | -0.5 | -Ï€/2 | -1 |
| bottom-right | 1 | 0.5 | Ï€/2 | 1 |

With zero type vectors, the example therefore yields [-1,0] and [1,0]. Equal geometric corners remain distinct tokens when their learned type vectors differ.

## Why this matters on a robot

Boxes from a detector can condition segmentation of a manipulation target. Applying the image resize twice or swapping corner ordering corrupts this interface. A valid prompt encoding does not guarantee that the resulting mask identifies the requested physical object.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2304.02643). [sam-point-prompt-encoding](/problems/sam-point-prompt-encoding)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.

Source verification: [official prompt-encoder implementation](https://github.com/facebookresearch/segment-anything/blob/main/segment_anything/modeling/prompt_encoder.py) confirms the half-pixel offset, normalized random Fourier position features, and distinct point/corner embeddings. The exercise code and fixtures are original.
