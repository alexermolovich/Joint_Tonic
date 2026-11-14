# Sample Terrain Difficulty by Policy Progress

## Intuition

A terrain curriculum changes difficulty from measured progress rather than a generic success label. Promotion and demotion use different distance tests, and completing the highest level triggers a recorded reassignment.

## Mathematical mechanism

Let $d_b=\|p_b-o_b\|_2$ be horizontal world displacement in meters, L the terrain length, command speed $s_b=\|c_b\|_2$ in m/s and episode duration T in seconds. On reset rows, $$U_b=[d_b>L/2],\qquad D_b=[d_b<s_bT/2]\land\neg U_b,\qquad \ell_b^*=\ell_b+U_b-D_b.$$ Promotion takes precedence. For K available levels, use $$\ell^{next}_b=\begin{cases}\lfloor u_bK\rfloor&\ell_b^*\ge K\\\max(\ell_b^*,0)&\ell_b^*<K,\end{cases}$$ with recorded $u_b\in[0,1)$. Other rows retain their old level and have false update flags. The command horizontal base-frame norm is invariant to a yaw rotation, while positions and origins share the world frame. This is the subsequent-reset update; terrain geometry and origin lookup remain separate.

## Visual computation trace

| Old level, K=3 | Distance at L=10 m | Decision | New level |
|---|---|---|---|
| 0 | 6 m | promote | 1 |
| 2 | 6 m | top-level completion, draw .4 | floor(.4*3)=1 |
| 0 | 0 m with positive command | demote but clamp low | 0 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

levels[0,2],positions[[6,0],[6,0]],origins0,command[[1,0],[1,0]],resetallTrue,length10,seconds10,num_levels3,draws[0,.4] -> move_up[True,True],move_downFalse,levels[1,1],reassigned[False,True],distance[6,6].

## Why this matters on a robot

Clipping at the maximum level changes the released curriculum by removing reassignment. Demoting a successful robot when command demand is high also changes the policy unless promotion takes precedence. Distance alone does not verify travel direction or gait safety.

## Physical contract and limits

Positions and terrain lengths use meters; velocities m/s; angular rates rad/s; contact forces N; durations seconds; normalized action and unit-gravity coordinates are dimensionless. Penalty terms retain the individual units stated in the contract. Each environment is independent. Supplied episode counters and reset flags refer to the same control transition. Terrain update occurs on subsequent resets; no wall-clock scheduling or simulator action is performed. Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.

Source: [primary paper](https://github.com/leggedrobotics/legged_gym/blob/master/legged_gym/envs/base/legged_robot.py). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
