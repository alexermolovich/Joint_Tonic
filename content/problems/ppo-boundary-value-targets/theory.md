# Compute Value Targets Across Episode Boundaries

## Intuition

A robot rollout can end because the task terminates or because collection hits a time limit. These boundaries need different value targets: a real terminal has no future return, while a time limit can bootstrap from the last observation without borrowing rewards from the next reset.

## Mathematical mechanism

Let R be the return target, r immediate reward, V the supplied next-observation value, d termination, c truncation and M validity. Set continuation $C_t=R_{t+1}$ only when the next slot is valid and $d_t=c_t=0$; otherwise $C_t=V_{t+1}$. Then $$R_t=r_t+\gamma(1-d_t)((1-\lambda)V_{t+1}+\lambda C_t).$$ Gamma and lambda are dimensionless in [0,1]; reward, V and R share reward units. Rows are independent sequences. Invalid slots are zero, and the final valid slot always uses its supplied next value as continuation.

## Visual computation trace

| Boundary at first transition | reward | next value | gamma | target |
|---|---|---|---|---|
| time-limit truncation | 1 | 10 | 0.5 | 6 |
| true termination | 1 | 10 | 0.5 | 1 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

rewards[[1,2]],nextvalues[[10,20]],no boundaries,allvalid,gamma.5,lam1 gives lasttarget12 and first7.

## Why this matters on a robot

Bootstrapping from the autoreset observation creates a target for a different physical state. Recursing across a truncation leaks the following episode’s reward into the previous one. Record the final observation and the two boundary flags explicitly.

## Physical contract and limits

Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units. Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits. Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.

Source: [primary paper](https://arxiv.org/abs/1707.06347). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
