# Assemble a Pre-Norm Vision Transformer Block

## Intuition

Pre-normalization feeds standardized features into each sublayer while preserving an unnormalized residual path. Attention mixes tokens; the MLP transforms each token independently after that mixing.

## Math and block flow

For token matrix $X\in\mathbb R^{N\times D}$, define per-row population mean $\mu$ and variance $s^2$. Layer norm is $\mathrm{LN}_i(X)=(X-\mu)/\sqrt{s^2+10^{-5}}\odot\gamma_i+\beta_i$, with learned vectors $\gamma_i,\beta_i\in\mathbb R^D$.
$$Z=\mathrm{LN}_0(X),\quad A=\operatorname{softmax}_{\mathrm{keys}}\left(\frac{(ZW_Q)(ZW_K)^\top}{\sqrt D}\right),\quad U=X+(AZW_V)W_O.$$
For hidden width $F$,
$$Y=U+\mathrm{GELU}(\mathrm{LN}_1(U)W_1+b_1)W_2+b_2,\qquad \mathrm{GELU}(h)=\tfrac12h[1+\operatorname{erf}(h/\sqrt2)].$$
The projection matrices have shapes $D\times D$, $W_1:D\times F$, $W_2:F\times D$. All features are dimensionless.

| Stage | Shape | Residual source |
|---|---|---|
| First LN and attention | N × D | original X |
| Attention scores | N × N | rows query, columns key |
| First residual | N × D | U=X+attention |
| Second LN and MLP | N × F then N × D | U |
| Final addition | N × D | no final normalization |

When attention and MLP weights are zero, Y=X. With only b2=[1,-1] nonzero, [2,4] becomes[3,3]. Applying a post-norm would break both residual examples. Subtracting each logit row's maximum before exponentiation preserves softmax while avoiding overflow.

## Why this matters on a robot

Patch tokens often feed a manipulation policy. Swapping pre/post-norm or the key axis changes checkpoint behavior despite identical tensor shapes. This one-head CPU block teaches ordering and residuals; it does not reproduce a trained ViT or its full multi-head architecture.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2010.11929). [vit-patch-class-tokens](/problems/vit-patch-class-tokens)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
