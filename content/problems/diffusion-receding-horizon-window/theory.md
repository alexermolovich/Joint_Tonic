# Execute a short window, then observe again

## Intuition

A policy may predict more actions than a controller should execute without new feedback. Receding-horizon control uses a short near-term window and replans after another observation. The predicted horizon and the executed horizon have different roles.

## Keep alignment explicit

Let $A\in\mathbb R^{B\times H\times D}$ contain trajectories with B independent examples, H ordered control ticks and D action channels. Let s be the caller-supplied start offset and K the number of ticks to execute. The selected commands are

$$
U_{bkd}=A_{b,s+k,d},\qquad 0\le k<K,\qquad s+K\le H.
$$

Validity $V\in\{0,1\}^{B\times H}$ must satisfy

$$
V_{b,s+k}=1\quad\text{for every }b,k.
$$

H, s and K are dimensionless tick counts. With controller period $\Delta t$ seconds, the selected buffer covers K control intervals. The function does not estimate timing from wall-clock arrival order or determine which prediction index is current.

## Visual: prediction versus execution

| Prediction offset | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| Predicted action | 10 | 20 | 30 | 40 |
| Selected with s=1, K=2 | — | 20 | 30 | — |
| Next observation | | | Replan after selected window | |

The static timeline shows exactly which entries are copied. It is also a text alternative, with no animation.

If a three-tick chunk has validity [True,True,False], selecting its first two ticks succeeds. Selecting offsets1 and2 fails as a unit. Dropping the invalid last tick would silently shorten the controller's agreed buffer.

## Why this matters on a robot

Executing an entire long chunk can compound error as objects move or contact changes. Executing too few ticks can make inference latency dominate. This function enforces the buffer's shape and availability; a separate scheduler measures latency and chooses K.

A common failure confuses padding with a zero action. Another applies the observation-history offset twice, beginning too far into the future. Keep alignment metadata and the controller period alongside every plan.

## Check your understanding

1. Why reject one missing selected tick instead of skipping it? Skipping changes timing and the agreed execution length.
2. Does this function prove the commands are safe? No; actuator and collision checks are separate.
3. Are invalid rows after the selected window an error? No, provided their numeric values satisfy the input contract.


## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2303.04137), SectionIII: receding-horizon control. Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset. This returns a command buffer for a synthetic controller; it does not drive a robot, run denoising or infer the observation-horizon offset.

Prerequisites: [ act-sliding-action-chunks ](/problems/act-sliding-action-chunks)


## Numerical shape trace

| Horizon index | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| Prediction | 10 | 20 | 30 | 40 |
| Selected, offset1 and length2 | — | 20 | 30 | — |
