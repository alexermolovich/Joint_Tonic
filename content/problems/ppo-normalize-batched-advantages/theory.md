# Normalize Batched Advantages

## Intuition

Different rollout batches can have very different advantage scales. Centering and rescaling the valid batch keeps the update scale interpretable, while the mask prevents padding or missing transitions from changing its statistics.

## Mathematical mechanism

For valid count $N=\sum M_{bt}$, define $$\mu=N^{-1}\sum M_{bt}A_{bt},\quad v=N^{-1}\sum M_{bt}(A_{bt}-\mu)^2,\quad Z_{bt}=M_{bt}\frac{A_{bt}-\mu}{\sqrt{v+\epsilon}}.$$ A has reward units; epsilon has squared reward units under the fixed numerical reward convention. Normalized Z is dimensionless. For N=0 set mean and variance to zero. This is a declared stabilization choice rather than an invariant of every PPO implementation.

## Visual computation trace

| Input | Valid | Contribution to mean | Output with epsilon1 |
|---|---|---|---|
| 1 | yes | 1/2 | -1/sqrt2 |
| 3 | yes | 3/2 | +1/sqrt2 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

advantages[[1,3]],valid[[True,True]],epsilon1 gives mean2,var1,stdsqrt2,normalized[-1/sqrt2,1/sqrt2].

## Why this matters on a robot

Normalizing over padded values changes the learning signal when episode lengths change. Normalizing each robot separately also changes relative weighting compared with a shared batch. A single valid transition centers to zero under this contract.

## Physical contract and limits

Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units. Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits. Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.

Source: [primary paper](https://arxiv.org/abs/1707.06347). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
