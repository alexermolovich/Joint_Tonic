# Reset Failed Locomotion Environments

## Intuition

Reset logic should identify why an episode ended before replacing state. A timeout and a forbidden body contact both restart an environment, but downstream value targets may treat them differently.

## Mathematical mechanism

For environment b and selected termination-contact body k, let $f_{bk}\in\mathbb R^3$ be its contact force in newtons. With control-step count $t_b$ and configured maximum T, $$F_b=\bigvee_k[\|f_{bk}\|_2>1\mathrm{\ N}],\quad H_b=[t_b>T],\quad R_b=F_b\lor H_b.$$ The strict inequalities follow the released termination convention; empty contact sets give false failure flags. Use the supplied initial state $x_b^0$ exactly where reset is true: $$x^{next}_b=\begin{cases}x_b^0&R_b\\x_b&\neg R_b.\end{cases}$$ Reset last actions, feet air-time histories and episode counters to zero on the same rows. Report both F and H even when both hold. This pure function does not generate randomized poses or commands, nor does it advance an unreset environment.

## Visual computation trace

| Contact magnitude | Steps / limit | Failure | Timeout | Reset |
|---|---|---|---|---|
| 1 N | 5 / 5 | False | False | False |
| 1.01 N | 5 / 5 | True | False | True |
| 0 N | 6 / 5 | False | True | True |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

B2,K1 contacts[[[1,0,0]],[[0,1.01,0]]], steps[5,5],max5, state[[2],[3]],initial[[0],[1]],last_action[[.2],[.3]],feet[[.1],[.2]] -> failure[False,True],timeout[False,False],reset[False,True],state[[2],[1]],last_action[[.2],[0]],feet[[.1],[0]],steps[5,0].

## Why this matters on a robot

Resetting physical state while retaining old actions or air-time counters contaminates the next episode. Collapsing timeout into contact failure loses information required for value bootstrapping. This component does not perform a real robot reset.

## Physical contract and limits

Positions and terrain lengths use meters; velocities m/s; angular rates rad/s; contact forces N; durations seconds; normalized action and unit-gravity coordinates are dimensionless. Penalty terms retain the individual units stated in the contract. Each environment is independent. Supplied episode counters and reset flags refer to the same control transition. Terrain update occurs on subsequent resets; no wall-clock scheduling or simulator action is performed. Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.

Source: [primary paper](https://github.com/leggedrobotics/legged_gym/blob/master/legged_gym/envs/base/legged_robot.py). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
