# Build and Evaluate a Bounded VLA Release

## Intuition

Frozen features reduce the trainable surface, but an adapter is useful only if its output is interpreted with the correct robot's action bounds. Explicit training and held-out masks prevent the integration from reporting its fitting loss as generalization evidence.

## Adapter update

For training features $X\in\mathbb R^{n\times D}$, frozen base $W\in\mathbb R^{D\times A}$, frozen projection $P\in\mathbb R^{D\times R}$, and trainable adapter $B\in\mathbb R^{R\times A}$,

$$\hat Y=XW+XPB,\quad L=\frac{\|\hat Y-Y\|_F^2}{nA},\quad B^+=B-\eta\frac{2}{nA}(XP)^\top(\hat Y-Y).$$

All features and normalized actions are dimensionless. $Y$ contains normalized training targets, $n$ counts selected training slots, $A$ counts action channels, and $\eta$ is the learning rate. This is a one-step linear teaching model; it is not transformer fine-tuning or full LoRA training because $P$ remains frozen.

## Action interpretation

For raw normalized scalar $a$, token $q$ and decoded normalized center $c$,

$$q=\min(15,\lfloor8(\operatorname{clip}(a,-1,1)+1)\rfloor),\qquad c=-1+(q+0.5)/8.$$

Each embodiment's physical bounds $l,u$ in radians give action $l+(c+1)(u-l)/2$. Quantization changes predictions even when the adapter fits exactly. In Example 1, raw 0.5 becomes token 12 and decoded action 0.5625, yielding squared error 0.00390625.

| Stage | Shape | Evidence |
| --- | --- | --- |
| Training selection | n by D | Valid training slots only |
| Adapter | R by A | One explicit gradient update |
| Generated action tokens | B by T by A | Invalid slots use -1 |
| Held-out slices | E and 3 | Missing slices stay NaN |

## Why this matters on a robot

An adapter and its normalization bounds form a serving contract. Swapping bounds changes commanded angles without changing the tokens. A good mean can hide a failing embodiment, so the gate checks every represented embodiment and task. Missing tasks remain an evidence gap in the reproducibility report; this bounded gate cannot certify unseen tasks.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2406.09246). [build-robot-sequence-validity-masks](/problems/build-robot-sequence-validity-masks) · [openvla-lora-policy-layer](/problems/openvla-lora-policy-layer) · [rt1-action-codec](/problems/rt1-action-codec)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
