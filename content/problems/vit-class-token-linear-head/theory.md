# Read a Normalized Class Token with a Linear Head

## Intuition

The class token summarizes a transformer sequence. This readout normalizes only that token across its channels and applies a linear classifier. Patch tokens remain in the input because they helped create the class token upstream, but this function must not average them again.

## Mathematics and physical meaning

The input $X$ has shape $(B,L,D)$: batches, tokens and dimensionless feature channels. Set $x=X_{b,0,:}$. Population layer normalization uses all $D$ channels:
$$\mu=\frac1D\sum_jx_j,\quad v=\frac1D\sum_j(x_j-\mu)^2,\quad h_j=\gamma_j\frac{x_j-\mu}{\sqrt{v+\epsilon}}+\beta_j.$$
Here $\gamma,\beta\in\mathbb R^D$ are supplied channel scale/offset and $\epsilon>0$ stabilizes the denominator. Use population variance, not a $D-1$ sample correction. A weight matrix $W\in\mathbb R^{D\times C}$ and bias $a\in\mathbb R^C$ produce
$$y=hW+a\in\mathbb R^C.$$
The output is $(B,C)$ logits; no softmax is applied. If $D=1$, centering gives zero and the answer reduces to $\beta W+a$, regardless of the token value.

## Visual trace

| Operation | Two-channel example |
|---|---|
| Class token | `[1,3]` |
| Mean / population variance | `2 / 1` |
| epsilon | `1` |
| Normalized token | `[-1/√2, 1/√2]` |
| Identity head, zero bias | unchanged |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** Class token `[1, 3]`, gamma `[1, 1]`, beta `[0, 0]`, identity head, zero bias and epsilon `1` produce logits `[[-1/sqrt(2), 1/sqrt(2)]]`.

**Example 2.** Any one-channel token, gamma `[2]`, beta `[3]`, weight `[[4]]`, bias `[5]` and epsilon `1e-8` produce `[[17]]`: the normalized one-channel value is zero.

## Why this matters on a robot

A frozen visual encoder can feed a small robot scene classifier. Averaging all tokens here changes the learned readout contract; normalizing across batches also makes one robot's prediction depend on another sample.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2010.11929). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
