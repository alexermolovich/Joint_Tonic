# Apply Paired-Image Self and Cross Attention

## Intuition

Self attention collects context within one image; cross attention compares the two images. Positive-feature attention can collect a key/value summary before visiting queries, avoiding a full pairwise attention matrix.

## Mathematics and conventions

For query sequence $X\in\mathbb R^{L\times D}$ and context $Y\in\mathbb R^{J\times D}$, use four supplied $D\times D$ matrices. Define $Q=\phi(XW_q)$, $K=\phi(YW_k)$, $V=YW_v$, with $\phi(z)=1+z$ for nonnegative z and $e^z$ otherwise. Mask invalid context rows, then compute

$$T=K^\top V,\quad k_\Sigma=\sum_jK_j,\quad M_i=\left(\frac{Q_iT}{\max(Q_i k_\Sigma,10^{-9})}\right)W_o.$$

T has shape $(D,D)$, the key sum shape $(D,)$, and each output message shape $(D,)$. Everything is dimensionless. Invalid queries get a zero message. After self residuals $A_1,B_1$, cross residuals are

$$A_2=A_1+M(A_1,B_1),\qquad B_2=B_1+M(B_1,A_1).$$

Both use the same pre-cross states. A positive denominator floor is an explicit numerical convention; it does not invent evidence when the entire context is masked. This is a teaching block, not the full LoFTR transformer layer.

## Visual computation trace

| Stage | Source D=1 | Target D=1 |
| --- | --- | --- |
| Input | 1 | 2 |
| Self residual | 1+1=2 | 2+2=4 |
| Frozen cross messages | target contributes4 | source contributes2 |
| Final | 6 | 6 |

## Worked examples

1. With all four weight matrices zero, outputs equal the supplied feature rows wherever valid and are zero elsewhere. The messages are zero.
2. D=1, all four weights 1, one valid source feature `[[1.]]`, one valid target feature `[[2.]]`: self_source is `[[2.]]`, self_target `[[4.]]`, and both final outputs are `[[6.]]`. Sequentially updating the target from an already updated source would be wrong.

## Why this matters on a robot

An accidental sequential cross update gives one image extra information and makes results depend on update order. Padding treated as real context can also dilute messages or introduce false feature evidence.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2104.00680). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
