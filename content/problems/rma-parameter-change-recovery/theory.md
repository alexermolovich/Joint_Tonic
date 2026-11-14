# Evaluate Policy Recovery After a Parameter Change

## Intuition

Recovery requires a sustained window of measured good tracking after the environment changes. Removing missing samples before counting would falsely join observations that were never consecutive.

## Mathematical mechanism

For normalized errors e, validity M, change index c, tolerance tau and integer hold length H, define $$g_{bt}=M_{bt}\land(e_{bt}\le\tau),\quad s_b=\min\{i\ge c:\sum_{t=i}^{i+H-1}g_{bt}=H\}.$$ Only complete windows in the recorded horizon qualify. Delay is $t_{s_b}-t_c$, the start of the first verified window, not its completion. No window yields index -1 and NaN delay. A separate post-change mean uses every valid error from c onward; absent evidence gives NaN. Time is seconds, errors dimensionless.

## Visual computation trace

| Timestamp | Error | Evidence |
|---|---|---|
| 1 s | 0.2 | exceeds tolerance 0.1 |
| 2 s | 0.1 | stable window starts |
| 3 s | 0.1 | two-sample hold verified |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Times [0, 1, 2, 3], errors [[2, 0.2, 0.1, 0.1]], all valid, change index 1, tolerance 0.1 and hold length 2 yield recovered true, index 2, delay 1 second, post-change mean 0.4/3 and count 3.

## Why this matters on a robot

A plausible latent can describe old terrain or a previous episode. Completion time differs from observation age, and recovery requires consecutive valid evidence.

## Physical contract and limits

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

Source: [primary paper](https://arxiv.org/abs/2107.04034). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
