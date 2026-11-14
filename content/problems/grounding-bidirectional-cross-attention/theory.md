# Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention

## Intuition

Image-to-text and text-to-image attention answer different questions. Each image token asks which words describe it; each word asks which image locations support it. The two directions share raw compatibility scores but normalize across different keys.

## Mathematics and physical meaning

For one batch item, projected image tokens $I\in\mathbb R^{P\times D}$ and text tokens $T\in\mathbb R^{Q\times D}$ are dimensionless. Shared scores are
$$S=IT^\top/\sqrt D.$$
For valid image query $p$, normalize only valid text keys $q$:
$$A_{pq}=\frac{e^{S_{pq}-m_p}}{\sum_{r\in\mathcal T}e^{S_{pr}-m_p}},\qquad m_p=\max_{r\in\mathcal T}S_{pr}.$$
Here $\mathcal T$ is the valid text-index set. Invalid queries or an empty key set produce exact zero rows, not NaN. Independently normalize $S^\top$ across valid image keys to obtain $B\in\mathbb R^{Q\times P}$.
$$I'=AT,\qquad T'=BI.$$
For batch size $N_b$, returned shapes are image context $(N_b,P,D)$, text context $(N_b,Q,D)$ and weights $(N_b,P,Q)$ and $(N_b,Q,P)$. Input code uses `B` for batch and `T` for text count. No learned projections, heads, residual gates or feed-forward layers are implemented here.

## Visual trace

| Direction | Query count | Valid key count | Uniform example weights |
|---|---:|---:|---|
| Image → text | 1 | 2 | `[.5,.5]` |
| Text → image | 2 | 1 | `[1]` for each word |
| Any query → no valid keys | any | 0 | all zero |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** One image token `[1]` and two text tokens `[0]`, `[0]`, all valid: image weights `[.5,.5]`, image context `[0]`; each text query has weight `[1]` and context `[1]`.

**Example 2.** Make both text tokens invalid. Image queries have no valid keys and text queries are invalid; every returned context and weight is zero, without NaNs.

## Why this matters on a robot

Language grounding connects a phrase such as 'red handle' to visible regions. Simply transposing image-to-text probabilities does not yield text-to-image probabilities. Including padded tokens can shift grounding even when the real words are unchanged.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2303.05499). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
