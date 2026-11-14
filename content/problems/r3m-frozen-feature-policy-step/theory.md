# Evaluate Frozen Features in a Small Policy

## Intuition

A frozen encoder can still support learning a new robot controller. Update only a small policy head, then evaluate it on rows that did not contribute gradients.

## Mathematical mechanism

Concatenate frozen visual features $Z\in\mathbb R^{N\times D}$ and normalized robot state $P\in\mathbb R^{N\times Q}$ into $X=[Z,P]$. An affine head predicts $\hat A=XW+b$, with $W\in\mathbb R^{(D+Q)\times A}$ and $b\in\mathbb R^A$. For the training subset T, residual matrix E and $n=|T|$, $$L_T=\frac{1}{nA}\sum_{i\in T,a}E_{ia}^2,\quad G_W=\frac{2X_T^\top E_T}{nA},\quad G_b=\frac{2\sum_{i\in T}E_i}{nA}.$$ Apply simultaneous SGD $$W^+=W-\eta G_W,\qquad b^+=b-\eta G_b.$$ Recompute predictions and training/evaluation losses using the updated parameters. Evaluation rows never enter either gradient; an empty evaluation set has NaN loss. All coordinates and MSE units are normalized and dimensionless. This affine head replaces the paper's larger behavior-cloning network for a small deterministic exercise.

## Visual computation trace

| One training row x=1, target=1, W=b=0 | Value |
|---|---|
| Residual | -1 |
| Weight/bias gradients | -2, -2 |
| Learning rate .1 gives W,b | .2, .2 |
| Held-out x=2 prediction | .6 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

features [[1],[2]], state empty(2,0), actions [[1],[0]], train [True,False], evaluate [False,True], weight [[0]], bias [0], lr0.1 -> weight[[0.2]], bias[0.2], predictions[[0.4],[0.6]], losses before1, train-after0.36, evaluation0.36.

## Why this matters on a robot

Allowing held-out actions into a gradient makes the evaluation optimistic. A frozen feature representation can omit contact detail that an affine head cannot recover. Action MSE is a supervised diagnostic, not measured rollout success.

## Physical contract and limits

Embedding coordinates, supplied logits, normalized robot state and normalized actions are dimensionless. Frame indices are ordinal positions, not timestamps in seconds. Triplets stay in one video and the negative comes from another. Policy rows are supplied observations with explicit training/evaluation membership; no temporal transitions are inferred. Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

Source: [primary paper](https://arxiv.org/html/2203.12601v3). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
