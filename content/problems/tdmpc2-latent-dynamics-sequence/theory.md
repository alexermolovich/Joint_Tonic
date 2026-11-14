# Roll Out a Latent Dynamics Sequence

## Intuition

Planning repeatedly feeds a predicted latent into the next transition. Keep each predicted state on the same groupwise simplex as the initial representation instead of drifting into unconstrained coordinates.

## Mathematical mechanism

Let z_t be a row latent vector, a_t a normalized action and W_z,W_a,b supplied affine parameters. The original teaching transition is $$u_{t+1}=z_tW_z+a_tW_a+b,\qquad z_{t+1}=\operatorname{SimNorm}(u_{t+1}).$$ SimNorm applies stable softmax independently within each consecutive group. Returned states have shape B by (H+1) by D; the first slice preserves the provided z_0 exactly. This affine transition isolates normalization and rollout ordering, while the released dynamics use a richer learned network.

## Visual computation trace

| Stage | Shape | Invariant |
|---|---|---|
| Initial latent | B,D | each group sums 1 |
| Affine logits | B,D | unconstrained scores |
| SimNorm | B,D | each group sums 1 again |
| State trace | B,H+1,D | includes exact initial state |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

state [[.5,.5]],actions[[[0]]],all weights/bias 0,group 2 ->two identical states [.5,.5].

## Why this matters on a robot

A planner can exploit model error or an overoptimistic terminal critic. Normalized latent groups and stable candidate weights do not prove that imagined contact behavior is physically achievable.

## Physical contract and limits

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

Source: [primary paper](https://arxiv.org/abs/2310.16828). [Pinned official implementation](https://github.com/nicklashansen/tdmpc2/tree/332f19e4aba4bffe2dc736f45ea7f7bdc585903a). The exercise states every deviation from its released data and numerical conventions.
