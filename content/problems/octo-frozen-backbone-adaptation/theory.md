# Add a Frozen-Backbone Adaptation Module

## Intuition

A small residual adapter can learn a correction while a useful pretrained map stays fixed. Compute the prediction with the original adapter, then update both low-rank matrices from the same loss so the step is mathematically well defined.

## Mathematical mechanism

Let $H=XA$ and $Z=XW+HC$, with squared loss $\mathcal L=\|Z-Y\|_F^2/(BD)$. The frozen backbone is represented by the supplied feature matrix and immutable base map W. $$G=2(Z-Y)/(BD),\qquad \nabla_C=H^TG,\qquad\nabla_A=X^TGC^T.$$ Return $A^+=A-\eta\nabla_A$ and $C^+=C-\eta\nabla_C$ together. This original linear teaching adapter does not claim Octo uses this exact architecture.

## Visual computation trace

| Stage | Scalar example |
|---|---|
| XW+(XA)C | 2*3+(2*1)*2=10 |
| target, loss | 8,4 |
| gradients dA,dC | 16,8 |
| lr0.1 update | A=-0.6,C=1.2 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

X=[[2]], W=[[3]], A=[[1]], C=[[2]], targets=[[8]], lr=0.1 returns prediction[[10]], loss4, down[[-0.6]], up[[1.2]]. W remains[[3]].

## Why this matters on a robot

An incorrect interface silently changes which sensor or actuator a feature describes. Preserve masks and schema versions when transferring to another robot.

## Physical contract and limits

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original linear residual-adapter training step motivated by adapting generalist policies while freezing pretrained weights; this is not Octo official fine-tuning code or a full parameter-efficient method.

Source: [primary paper](https://arxiv.org/abs/2405.12213). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
