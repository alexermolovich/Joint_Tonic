# Evaluate an MPC Tracking Cost

## Intuition

An MPC planner compares candidate futures using one scalar objective. The stage penalty rewards tracking during motion, the effort penalty discourages aggressive commands, and the terminal penalty values where the horizon ends.

## Mathematics and physical meaning

For predicted state $x_k\in\mathbb R^D$, target $r_k$, control $u_k\in\mathbb R^M$, and nonnegative diagonal weight vectors $q,s,p$, define $e_k=x_k-r_k$. The discrete cost is
$$J=\sum_{k=0}^{N-1}\left(\sum_{d=1}^D q_d e_{kd}^2+\sum_{j=1}^M s_j u_{kj}^2\right)+\sum_{d=1}^D p_d e_{Nd}^2.$$
Weights carry inverse squared units of their corresponding variable, making the cost dimensionless. When $N=0$, only the terminal term remains. This evaluates supplied trajectories; it does not solve the optimization or simulate dynamics.

## Visual trace

| Term, states [1,2,3], targets 0 | Weighted cost |
|---|---|
| Stage states 1,2 with q=1 | 1+4=5 |
| Controls 1,2 with s=2 | 2+8=10 |
| Terminal state 3 with p=3 | 27 |
| Total | 42 |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `states=[[1],[2],[3]], targets=zeros((3,1)), controls=[[1],[2]], state_weights=[1], control_weights=[2], terminal_weights=[3]` → `42.0`.
2. `states=[[2,-1]], targets=[[0,0]], controls=empty((0,1)), state_weights=[9,9], control_weights=[1], terminal_weights=[2,3]` → `11.0`.

## Why this matters on a robot

Mixing metres and radians without explicit weights changes behavior when units change. A low cost alone is not a safety certificate: collision and actuator constraints must be checked separately.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
