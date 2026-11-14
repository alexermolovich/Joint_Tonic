# Track the Age of an Asynchronous Adaptation Latent

## Intuition

A newly completed adaptation job can still describe old observations. Track completion age separately from evidence age so a controller does not confuse computation availability with freshness.

## Mathematical mechanism

At control time t, select $$j^*(t)=\max\{j:c_j\le t\},\quad a_{obs}=t-o_{j^*},\quad a_{done}=t-c_{j^*}.$$ Completion c and observation o use seconds on one clock with o<=c. Completion times increase, but observation times may go backward when asynchronous jobs finish out of order. Use the selected latent only if observation age is at most the bound. This latest-completion policy does not fall back to an earlier job, even if that job used fresher observations.

## Visual computation trace

| Job | Observation | Completion | At control 0.7 s |
|---|---|---|---|
| 0 | 0.49 | 0.5 | earlier job |
| 1 | 0.1 | 0.6 | selected, evidence age 0.6 s |
| Max age 0.3 s | stale evidence | available job | context zero |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Control time 1, completion time 0.9, observation time 0.5, latent [2] and maximum age 0.4 produce index 0, observation age 0.5, completion age approximately 0.1, usable false and zero context.

## Why this matters on a robot

A plausible latent can describe old terrain or a previous episode. Completion time differs from observation age, and recovery requires consecutive valid evidence.

## Physical contract and limits

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

Source: [primary paper](https://arxiv.org/abs/2107.04034). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
