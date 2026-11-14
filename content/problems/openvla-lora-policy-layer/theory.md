# Add Low-Rank Adaptation to a Policy Layer

## Intuition

Adapting a large policy need not update every entry of a pretrained matrix. A low-rank branch represents a restricted weight change with two smaller matrices. The base calculation still matters to input gradients even when its parameters are frozen.

## Shapes and scaling

Let a token row be $x\in\mathbb R^I$ and the frozen base weight be $W\in\mathbb R^{O\times I}$. A down-projection $A\in\mathbb R^{r\times I}$ and up-projection $B\in\mathbb R^{O\times r}$ define

$$
\Delta W=\frac{\alpha}{r}BA,\qquad
y=xW^\top+\frac{\alpha}{r}(xA^\top)B^\top.
$$

I and O are input/output widths, r is the adapter rank, and nonnegative alpha is a dimensionless scale. The batch/token axes are carried through unchanged. The factorization introduces $r(I+O)$ adapter entries; when r is small this can be fewer than IO full-weight entries. It does not guarantee faster unmerged inference.

## Visual: the rank-one calculation

| Branch stage | Example value |
|---|---|
| Base projection of [1,2] | [1,2] |
| Down-project by [1,-1] | -1 |
| Up-project by [2,3] | [-2,-3] |
| Scale by alpha/r = 2 | [-4,-6] |
| Add base result | [-3,-4] |

This original table is a static computation graph and text alternative. The adapter changes feature coordinates, not actuator commands or physical units.

## Freeze parameters without cutting input gradients

Use W as a constant while differentiating the output. For an output-gradient row $g=\partial L/\partial y$, the input gradient is

$$
\frac{\partial L}{\partial x}
=g\left(W+\frac{\alpha}{r}BA\right),\qquad
\frac{\partial L}{\partial W}=0\quad\text{under the declared frozen-parameter rule}.
$$

Detaching the complete base output would incorrectly remove gW from the input gradient. Detach only the base weight for this operation, without changing its caller-owned requires_grad setting.

When B is initially zero, the forward adapter update is zero and the A gradient is zero, but B can receive a nonzero gradient through xA^T. In example 2 that hidden value is 7, giving gradient 7 to each up-projection entry for a summed output. Preserve those autograd connections even when alpha is zero.

## Why this matters on a robot

Parameter-efficient fine-tuning can make adaptation feasible with less trainable state. It still needs task and embodiment evaluation. Applying the adapter with the wrong rank scaling, omitting it at inference, or accidentally updating the supposedly frozen base changes the deployed policy.

## Questions

Does a frozen W prevent gradients to x? No; x still passes through the constant base map. Does a zero initial update prevent learning? Not necessarily; the up-projection can already have a nonzero gradient.

Sources: [OpenVLA parameter-efficient fine-tuning](https://arxiv.org/html/2406.09246v3#S5.SS3), [LoRA](https://arxiv.org/abs/2106.09685), and the [official LoRA linear layer](https://github.com/microsoft/LoRA/blob/main/loralib/layers.py). This original function isolates one adapter and does not copy source implementation code.
