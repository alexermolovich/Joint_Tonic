# Apply Groupwise SimNorm to Latent States

## Intuition

SimNorm turns each small latent block into a probability simplex. Different blocks retain separate capacity; treating the entire vector as one softmax changes the representation.

## Mathematical mechanism

For a row with D entries and group width G dividing D, reshape it into D/G groups. In each group, $$z_{gc}=\frac{\exp(x_{gc}-m_g)}{\sum_j\exp(x_{gj}-m_g)},\qquad m_g=\max_jx_{gj}.$$ Each group sums to1 and has nonnegative entries. Subtracting the group maximum preserves ratios while preventing exponential overflow. All latent coordinates are dimensionless; return the original B by D layout.

## Visual computation trace

| Raw group | Stable exponentials | Normalized group |
|---|---|---|
| [0,log(3)] | [1/3,1] | [.25,.75] |
| [1000,1000] | [1,1] | [.5,.5] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

latents[[0,0,1,1]],group 2 ->[[.5,.5,.5,.5]].

## Why this matters on a robot

A planner can exploit model error or an overoptimistic terminal critic. Normalized latent groups and stable candidate weights do not prove that imagined contact behavior is physically achievable.

## Physical contract and limits

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

Source: [primary paper](https://arxiv.org/abs/2310.16828). [Pinned official implementation](https://github.com/nicklashansen/tdmpc2/tree/332f19e4aba4bffe2dc736f45ea7f7bdc585903a). The exercise states every deviation from its released data and numerical conventions.
