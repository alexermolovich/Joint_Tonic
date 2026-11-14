# Detect Phase Misalignment in a Motion Clip

## Intuition

Two phases close to opposite ends of a cyclic clip can still describe nearly the same point in the motion. Measure the shortest circular error instead of subtracting clip fractions as ordinary linear coordinates.

## Mathematical mechanism

For observed phase o and reference phase r in $[0,1)$, $$e=((o-r+\tfrac12)\bmod1)-\tfrac12.$$ Error e is a dimensionless clip fraction in $[-1/2,1/2)$; the ambiguous half-cycle is represented as -1/2. For Boolean mask M, flag $M\land(|e|>\tau)$ and report the mean absolute valid error per batch row. Missing errors and missing row means are NaN, not evidence of perfect alignment. Equal threshold values pass.

## Visual computation trace

| Observed | Reference | Linear difference | Circular difference |
|---|---|---|---|
| 0.99 | 0.01 | 0.98 | -0.02 |
| 0.50 | 0 | 0.50 | -0.50 by tie rule |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Observed phase [[0.99]], reference [[0.01]], valid [[True]] and threshold 0.03 give error [[-0.02]], misaligned [[False]], mean_absolute [0.02] and counts [1].

## Why this matters on a robot

A robot can receive a high imitation score while violating actuator or contact constraints. Inconsistent frame conventions or quaternion signs can also create artificial motion error.

## Physical contract and limits

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

Source: [primary paper](https://arxiv.org/abs/1804.02717). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
