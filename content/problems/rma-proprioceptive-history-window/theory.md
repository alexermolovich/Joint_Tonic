# Window Proprioceptive History

## Intuition

Adaptation history records what the robot observed and did before the current decision. Left-pad missing history instead of borrowing from another episode or including the current command.

## Mathematical mechanism

For query record t and history length H, candidate indices are $$r_k=t-H+k,\qquad k=0,\ldots,H-1.$$ Retain a row only if it is nonnegative and shares the query episode. Nondecreasing episode IDs select the preceding suffix of the current episode. A retained feature is $[o_{r_k},a_{r_k}]$; padding uses zeros and source index -1. Output shape is Q by H by (O+A). Record t is excluded, preventing current-command leakage.

## Visual computation trace

| Query | H=3 candidate rows | History |
|---|---|---|
| 2, same episode | -1,0,1 | padding,row0,row1 |
| first new-episode row | earlier episode | padding only |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Observations [[1], [2], [3]], actions [[0.1], [0.2], [0.3]], episode IDs [0, 0, 0], query [2] and H=3 produce history [[[0, 0], [1, 0.1], [2, 0.2]]], validity [[False, True, True]] and indices [[-1, 0, 1]].

## Why this matters on a robot

A plausible latent can describe old terrain or a previous episode. Completion time differs from observation age, and recovery requires consecutive valid evidence.

## Physical contract and limits

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

Source: [primary paper](https://arxiv.org/abs/2107.04034). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
