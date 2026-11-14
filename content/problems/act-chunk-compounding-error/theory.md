# Evaluate Chunk Length Against Compounding Error

## Intuition

Open-loop action errors accumulate until feedback corrects them. A small reset-and-integrate model makes the effect of different feedback intervals visible without pretending to simulate a full robot.

## Mathematical mechanism

For length L and step t, let 

$$b=L\lfloor t/L\rfloor$$

 be its chunk start. Position error is $e_t^{(L)}=\sum_{s=b}^{t}\delta_s$, with $\delta_s\in\mathbb R^D$ supplied increment error. Report $J_L=(TD)^{-1}\sum_{t,d}(e_{t,d}^{(L)})^2$. This diagnostic assumes perfect reset at boundaries and a unit-gain position integrator.

## Visual computation trace

| Length | Accumulated errors for [1,1,1] | Mean square |
|---|---|---|
| 1 | [1,1,1] | 1 |
| 2 | [1,2,1] | 2 |
| 3 | [1,2,3] | 14/3 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

action_error=[[1],[1],[1]], chunk_lengths=[1,2,3] returns [1,2,14/3]. The last length2 chunk contains only the final sample.

## Why this matters on a robot

Longer chunks do not always increase measured error because residuals can cancel. Real feedback is not a perfect reset, and perception delays may shift the boundary. Keep this diagnostic separate from task-success evaluation and compare it against actual rollout slices.

## Physical contract and limits

Error channels are normalized dimensionless position increments; all channels are equally weighted, not mixed raw meters and radians. Rows are equally spaced control steps. The toy reset represents perfect feedback at each chunk boundary. Original diagnostic inspired by ACT compounding-error motivation. It evaluates supplied residuals in a unit-gain integrator; it does not predict ACT rollout performance or claim an optimal chunk length.

Source: [primary paper](https://arxiv.org/abs/2304.13705). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
