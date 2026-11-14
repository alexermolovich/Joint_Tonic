# Estimate a Latent Dynamics Context

## Intuition

A temporal adaptation module turns normalized sensor/action history into policy context. Mask padding before temporal mixing and suppress empty histories instead of treating a learned bias as fresh evidence.

## Mathematical mechanism

Let X have shape B by H by F and M a left-padding mask. Zero invalid rows and pad one time slot on each side. Then $$C_{btc}=\sum_{k=0}^{2}\sum_f\widetilde X_{b,t+k,f}K_{kfc},\quad A_{btc}=M_{bt}\max(C_{btc},0).$$ Flatten A chronologically and apply $z_b=\operatorname{vec}(A_b)W+b$. An entirely invalid history gives zero latent and used=False. Features and latents are dimensionless. This supplied one-block model is an original surrogate, not the trained RMA temporal network.

## Visual computation trace

| Stage | Shape | Padding |
|---|---|---|
| History | B,H,F | zero invalid rows |
| Temporal block | B,H,C | ReLU and re-mask |
| Flatten | B,H*C | chronological |
| Latent head | B,L | zero absent history |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

With B=H=F=C=L=1, history value 2, center kernel weight 3, head weight 4 and bias 1, the latent is 25 and used is true.

## Why this matters on a robot

A plausible latent can describe old terrain or a previous episode. Completion time differs from observation age, and recovery requires consecutive valid evidence.

## Physical contract and limits

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

Source: [primary paper](https://arxiv.org/abs/2107.04034). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
