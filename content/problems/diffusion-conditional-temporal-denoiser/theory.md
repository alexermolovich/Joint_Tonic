# Build a Conditional Action Denoiser

## Intuition

An action denoiser uses both a noisy action window and observation context. A temporal kernel mixes nearby actions; a conditioning vector changes each hidden channel's scale and offset. This original one-block network isolates that mechanism without pretending to train a full policy.

## Mathematics and physical meaning

Noisy normalized actions $A$ have shape $(B,H,U)$ for batch, horizon and action channels. Zero-pad one step at each end, giving $\widetilde A$. With kernel $K\in\mathbb R^{3\times U\times C}$, cross-correlation is
$$V_{btc}=\sum_{k=0}^{2}\sum_{u=0}^{U-1}\widetilde A_{b,t+k,u}K_{kuc}.$$
Do not reverse the kernel. Supplied diffusion level $s_b\in[0,1]$ is not robot elapsed time. For observation context $o_b\in\mathbb R^F$, form
$$e_b=[\sin(\pi s_b),\cos(\pi s_b)],\qquad [\gamma_b,\beta_b]=o_bW_o+e_bW_s.$$
The two weight matrices have shapes $(F,2C)$ and $(2,2C)$; the first $C$ output channels are $\gamma$, the last $C$ are $\beta$. Apply feature-wise affine conditioning and SiLU:
$$Z_{btc}=(1+\gamma_{bc})V_{btc}+\beta_{bc},\quad h=Z\,\operatorname{sigmoid}(Z),\quad \widehat\epsilon=hW_h+a.$$
Here $W_h\in\mathbb R^{C\times U}$ and $a\in\mathbb R^U$ return predicted noise $(B,H,U)$. All features/actions are dimensionless normalized values. For numerical stability set $r=e^{-|Z|}$ and evaluate sigmoid as $1/(1+r)$ for nonnegative $Z$, otherwise $r/(1+r)$. There is no residual action addition, reverse sampler, optimizer or trained U-Net in this task.

## Visual trace

| Step | One action/channel, zero conditioning |
|---|---|
| Action / center kernel | `1 / 1` |
| Temporal response | `1` |
| FiLM scale / shift | `1 / 0` |
| SiLU | `1/(1+exp(-1))` |
| Identity head, zero bias | same predicted noise |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** Actions `[[[0]]]`, all-zero kernel and conditioning/time weights, head `[[1]]`, bias `[2]`: output predicted noise is `[[[2]]]`.

**Example 2.** Use action value `1`, center kernel value `1`, other kernel entries zero, head `1`, bias `0` and zero conditioning/time weights. Output is `[[[1/(1+exp(-1))]]]`, approximately `[[[0.73105858]]]`; do not add the original action.

## Why this matters on a robot

Temporal conditioning helps an action sequence reflect current observations. Kernel reversal changes which neighbor influences a command; confusing diffusion level with wall-clock time changes the model input. Predicted noise is not an executable robot command and needs a separate sampler and safety checks.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2303.04137). This explanation, table and code are original.

- [diffusion observation window encoder](/problems/diffusion-observation-window-encoder)
