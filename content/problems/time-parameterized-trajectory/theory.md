# Interpolate a Time-Parameterized Trajectory

## Intuition

Waypoints specify where an arm should be at particular times. Linear interpolation supplies positions between waypoints, while the segment slope exposes sudden velocity changes that positions alone can hide.

## Mathematics and physical meaning

For a query $t$ in segment $[t_k,t_{k+1}]$, let $\Delta t_k=t_{k+1}-t_k>0$ and $\alpha=(t-t_k)/\Delta t_k$. Joint vectors $q_k\in\mathbb R^D$ are radians. Return
$$q(t)=(1-\alpha)q_k+\alpha q_{k+1},\qquad \dot q(t)=\frac{q_{k+1}-q_k}{\Delta t_k}.$$
The derivative is radians/second and is constant inside each segment. At a corner the classical derivative is undefined; this API deliberately chooses the right segment, except at the final endpoint.

## Visual trace

| Query t (s), knots (0,0),(1,2),(3,4) | Position (rad) | Reported slope (rad/s) |
|---|---|---|
| 0.5 | 1 | 2 |
| 1 | 2 | 1 (right segment) |
| 3 | 4 | 1 (last segment) |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `times=[0,1,3], positions=[[0],[2],[4]], queries=[0.5,1,3]` → positions `[[1],[2],[4]]`, velocities `[[2],[1],[1]]`.
2. `times=[0,2], positions=[[0,2],[4,0]], queries=[2,0]` → positions `[[4,0],[0,2]]`, velocities `[[2,-1],[2,-1]]`.

## Why this matters on a robot

A geometrically smooth-looking path can demand an instantaneous velocity jump at a knot. This exercise exposes those slopes; it does not create an acceleration-limited or collision-safe command.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.

Adjacent knot intervals must be at least 1e-9 seconds; smaller intervals raise ValueError.
