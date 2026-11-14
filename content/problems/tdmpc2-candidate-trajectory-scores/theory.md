# Score Candidate Action Trajectories

## Intuition

A candidate plan earns predicted rewards until its first terminal transition. Its terminal critic estimate contributes only if the complete planned horizon remains alive.

## Mathematical mechanism

For candidate k, reward r_kt and terminal indicator d_kt, define survival before step t by $$A_{kt}=\prod_{j<t}(1-d_{kj}).$$ With horizon H and supplied terminal value V_k, $$J_k=\sum_{t=0}^{H-1}\gamma^t A_{kt}r_{kt}+\gamma^H A_{kH}V_k.$$ The reward on the terminating transition is included because survival uses only earlier flags. For H=0 the empty product equals1 and J equals V. Scores use reward units; survival and discounts are dimensionless. This isolates score assembly from neural prediction and action generation.

## Visual computation trace

| Horizon evidence | Reward contribution | Tail contribution |
|---|---|---|
| Rewards1,2;gamma .5 | 1+1 | .25*4=1 |
| First transition terminates | 1+0 | 0 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

rewards[[1,2]],no termination,terminal 4,gamma .5 ->contributions [1,1],tail 1,score 3.

## Why this matters on a robot

A planner can exploit model error or an overoptimistic terminal critic. Normalized latent groups and stable candidate weights do not prove that imagined contact behavior is physically achievable.

## Physical contract and limits

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

Source: [primary paper](https://arxiv.org/abs/2310.16828). [Pinned official implementation](https://github.com/nicklashansen/tdmpc2/tree/332f19e4aba4bffe2dc736f45ea7f7bdc585903a). The exercise states every deviation from its released data and numerical conventions.
