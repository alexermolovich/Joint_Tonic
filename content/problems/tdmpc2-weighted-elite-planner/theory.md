# Update a Sampling-Based Planner

## Intuition

A sampling planner concentrates its next proposal around high-scoring candidate sequences. Weighted population variance must be measured around the newly computed mean before enforcing exploration bounds.

## Mathematical mechanism

Select E valid elites by descending score and stable index ties. With inverse temperature beta>=0, $$w_i=\frac{\exp(\beta(J_i-J_{max}))}{\sum_j\exp(\beta(J_j-J_{max}))},\qquad\mu_{ta}=\sum_iw_i u_{ita},$$ $$\sigma_{ta}=\operatorname{clip}\!\left(\sqrt{\sum_iw_i(u_{ita}-\mu_{ta})^2},\sigma_{min},\sigma_{max}\right).$$ The mean and standard deviation have normalized action units. Beta has reciprocal score units, so exponential arguments are dimensionless. At least one shifted score is zero, ensuring a positive normalization denominator without adding an epsilon. This is one deterministic proposal update; it does not execute or choose a physical action.

## Visual computation trace

| Elites | Weights | Mean/std |
|---|---|---|
| Actions+1,-1; scoreslog(3),0 | .75,.25 | mean .5, std sqrt(.75) |
| Same data, maximumstd .5 | unchanged weights | std clipped.5 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Two scalar actions-1,+1, scores equal,all valid,E2,inverse_temperature 1,min_std 0,max_std 2 ->weights [.5,.5],mean 0,std 1.

## Why this matters on a robot

A planner can exploit model error or an overoptimistic terminal critic. Normalized latent groups and stable candidate weights do not prove that imagined contact behavior is physically achievable.

## Physical contract and limits

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

Source: [primary paper](https://arxiv.org/abs/2310.16828). [Pinned official implementation](https://github.com/nicklashansen/tdmpc2/tree/332f19e4aba4bffe2dc736f45ea7f7bdc585903a). The exercise states every deviation from its released data and numerical conventions.
