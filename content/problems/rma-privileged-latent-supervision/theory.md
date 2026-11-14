# Build Privileged Dynamics-Latent Supervision

## Intuition

Privileged simulator factors provide supervision that is unavailable on the deployed robot. Keep their teacher encoding fixed while measuring the adaptation prediction error.

## Mathematical mechanism

For normalized factors E of shape B by P, fixed weight W and bias b, define $Z=\tanh(EW+b)$. For predictions H of shape B by L and Boolean row mask M, $$\ell_i=\frac1L\sum_j(H_{ij}-Z_{ij})^2,\quad L_{adapt}=\frac1N\sum_iM_i\ell_i,\quad\nabla_HL=\frac{2M(H-Z)}{NL}.$$ N counts valid rows. Invalid targets/gradients are zero and per-state losses NaN; empty support has loss zero. Latents are dimensionless. The one-layer tanh teacher is an explicit surrogate, not the released RMA encoder.

## Visual computation trace

| Input | Role | Deployment |
|---|---|---|
| Simulator factors | fixed teacher input | unavailable |
| Encoded target | adaptation supervision | inferred instead |
| History prediction | student output | sensor-derived |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

One factor 0, weight 1, bias 0, prediction 2 and a valid row yield teacher target 0, per-state and total loss 4, and prediction gradient 4.

## Why this matters on a robot

A plausible latent can describe old terrain or a previous episode. Completion time differs from observation age, and recovery requires consecutive valid evidence.

## Physical contract and limits

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

Source: [primary paper](https://arxiv.org/abs/2107.04034). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
