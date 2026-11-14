# Build Distributional Reward and Ensemble-Value Targets

## Intuition

A target critic ensemble can reduce optimistic bootstrapping, while transformed two-hot targets keep large returns from becoming arbitrary regression scales. Record which critics supplied the target so it can be reproduced.

## Mathematical mechanism

For row b, recorded distinct critic indices i_b,j_b select decoded next-state values Q. Define $$v_b=\min(Q_{b,i_b},Q_{b,j_b}),\qquad y_b=r_b+\gamma(1-d_b)v_b,$$ where d is a Boolean terminal indicator and gamma the discount. Encode both r and y with $$s(x)=\operatorname{sign}(x)\log(1+|x|),\qquad w_l=\frac{b_h-s(x)}{b_h-b_l},\quad w_h=1-w_l,$$ after clipping the transformed value to the supplied bin support. Exact bin centers are one-hot. The reported bootstrap remains v even on terminal rows, but the target omits it. The official implementation samples one critic pair across the batch; per-row recorded pairs are an explicit deterministic generalization here.

## Visual computation trace

| Target stage | Example | Result |
|---|---|---|
| Select critics | [2,10,4], IDs 0 and 2 | minimum 2 |
| Bootstrap | reward 1,discount .5 | target 2 |
| Terminal transition | same values | target 1 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

reward 1,next_values [2,10,4],indices [0,2],not terminated,gamma .5 ->bootstrap 2,td_target 2. With bins[0,log(2),log(3)],reward target [0,1,0],value target [0,0,1].

## Why this matters on a robot

A planner can exploit model error or an overoptimistic terminal critic. Normalized latent groups and stable candidate weights do not prove that imagined contact behavior is physically achievable.

## Physical contract and limits

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

Source: [primary paper](https://arxiv.org/abs/2310.16828). [Pinned official implementation](https://github.com/nicklashansen/tdmpc2/tree/332f19e4aba4bffe2dc736f45ea7f7bdc585903a). The exercise states every deviation from its released data and numerical conventions.
