# Encode Positive and Negative Point Prompts

## Intuition

The same pixel can mean “include this” or “exclude this.” Positional features describe where the prompt lies; a learned type vector describes its meaning. Keep those signals separate until addition.

## Math and tensor trace

For pixel-index point $p_i=(x_i,y_i)$, image width $W$ and height $H$, define centered normalized coordinates $q_i=2(p_i+0.5)/[W,H]-1$. Frequencies $B\in\mathbb R^{2\times F}$ are supplied, as are type vectors $E\in\mathbb R^{2\times2F}$.
$$\theta_i=2\pi q_iB,\qquad z_i=[\sin\theta_i;\cos\theta_i]+E_{\ell_i},\quad \ell_i\in\{0,1\}.$$
Division is coordinatewise. $q$, frequencies, phase in radians and embedding values are dimensionless. Concatenation is along channels, not prompts.

| Step | Shape | Meaning |
|---|---|---|
| Pixel centers | N × 2 | x+0.5,y+0.5 |
| Fourier phases | N × F | Position-dependent phase |
| Sine then cosine | N × 2F | Smooth position features |
| Type addition | N × 2F | Positive/negative semantics |

For a one-pixel image, coordinate [0,0] becomes normalized [0,0], so all sine values are zero and cosine values one. A positive type vector [2,3] therefore yields [2,4] for F=1. No random frequencies are resampled between calls.

## Why this matters on a robot

Interactive segmentation can guide which object a robot should consider. Swapping x/y normalization on a nonsquare image misplaces prompts; swapping type rows reverses include/exclude semantics. Coordinates must already match the encoder's resized image. This isolates sparse encoding, not segmentation quality.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2304.02643). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.

Source verification: [official prompt-encoder implementation](https://github.com/facebookresearch/segment-anything/blob/main/segment_anything/modeling/prompt_encoder.py) confirms the half-pixel offset, normalized random Fourier position features, and distinct point/corner embeddings. The exercise code and fixtures are original.
