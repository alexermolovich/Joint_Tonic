# Route Inputs Through a Dual-System Policy Interface

## Intuition

A semantic model and a motor model need different inputs and may run at different rates. Preserve the semantic features, project state using the robot-specific interface, and report whether the cached context is fresh enough for the current observation.

## Mathematical mechanism

For semantic context $h_b\in\mathbb R^C$, state $s_b\in\mathbb R^S$, embodiment e and projection $P_e\in\mathbb R^{S\times E}$, $$c_b=[h_b;s_bP_{e_b}],\quad\Delta t_b=t_b^{obs}-t_b^{context},\quad ready_b=\mathbf1[0\le\Delta t_b\le T_{max}].$$ The head ID carries embodiment identity beyond the projection. Stale context remains diagnosable, but the readiness flag forbids its use under this interface.

## Visual computation trace

| Route | Source | Output |
|---|---|---|
| semantic | context [5] | [5] |
| motor | state[2], projector[3] | [6] |
| combined | same embodiment0 | [5,6] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

context=[[5]],state=[[2]],IDs=[0],projectors=[[[3]]],context_time=[1],observation_time=[1.2],max_age=.5 returns conditioning[[5,6]],head_ids[0],age[.2],ready[True].

## Why this matters on a robot

Aggregating incompatible robot channels or source types can hide a failing embodiment. Keep provenance, masks and per-slice results visible throughout training and evaluation.

## Physical contract and limits

Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates. Physical timestamps and maximum context age are seconds on one synchronized monotonic clock; no cross-device clock correction. Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

Source: [primary paper](https://arxiv.org/abs/2503.14734). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
