# Update a Receding-Horizon Control Sequence

## Intuition

A receding-horizon controller improves a whole sequence but executes only its first command. The remaining plan becomes the warm start for the next observation, with an explicit policy for the new final slot.

## Mathematics and conventions

For nominal controls $u_{td}$ and perturbations $\epsilon_{ktd}$ in rad/s, and dimensionless rollout weights $w_k$,

$$\tilde u_{td}=\operatorname{clip}\left(u_{td}+\sum_k w_k\epsilon_{ktd},l_d,h_d\right).$$

The action is $\tilde u_0$. The next plan satisfies $u^+_t=\tilde u_{t+1}$ for $t<H-1$, and $u^+_{H-1}=\tilde u_{H-1}$. Here $H$ counts control steps and $D$ joint channels. No conversion to position occurs without a dynamics model and time interval.

## Visual computation trace

| Slot | Updated command | Receded plan |
| --- | --- | --- |
| 0 | 0.5 rad/s, returned action | 2 rad/s |
| 1 | 2 rad/s after clipping | 2 rad/s repeated |

## Worked examples

1. Controls `[[0.],[1.]]`, perturbations `[[[2.],[0.]],[[0.],[2.]]]`, weights `[0.25,0.75]`, limits `[-1.]` to `[2.]`: updated `[[0.5],[2.]]`, action `[0.5]`, next plan `[[2.],[2.]]`.
2. One-step control `[[3.]]`, one zero perturbation, weight `[1.]`, limits `[-1.]` to `[1.]`: updated `[[1.]]`, action `[1.]`, next plan `[[1.]]`, all independent arrays.

## Why this matters on a robot

Executing the entire optimized sequence open-loop discards the feedback advantage of receding-horizon control. Returning an action view can also let later plan edits silently alter the command a caller intended to execute.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1509.01149). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
