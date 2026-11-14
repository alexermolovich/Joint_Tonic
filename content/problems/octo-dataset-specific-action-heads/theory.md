# Route Tokens into Dataset-Specific Action Heads

## Intuition

Two robots can share a policy representation while having different action widths. Route each readout through the correct robot head and explicitly mark which padded output channels describe real actuators.

## Mathematical mechanism

For example b routed to $g=d_b$, readout $z_b\in\mathbb R^E$, head $W_g\in\mathbb R^{E\times D}$ and bias $c_g$, $$a_{bj}=\begin{cases}(z_bW_g+c_g)_j,&j<n_g,\\0,&j\ge n_g.\end{cases}$$ Availability $M_{bj}$ is $j<n_g$, independent of whether an action value equals zero.

## Visual computation trace

| Dataset | Head result | Declared dimensions | Padded result |
|---|---|---|---|
| 0 | [3,5] | 1 | [3,0] |
| 1 | [7,9] | 2 | [7,9] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

readouts=[[2],[2]], IDs=[0,1], weights=[[[1,2]],[[3,4]]], biases=[[1,1],[1,1]], dimensions=[1,2] gives actions=[[3,0],[7,9]], available=[[True,False],[True,True]].

## Why this matters on a robot

An incorrect interface silently changes which sensor or actuator a feature describes. Preserve masks and schema versions when transferring to another robot.

## Physical contract and limits

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy.

Source: [primary paper](https://arxiv.org/abs/2405.12213). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
