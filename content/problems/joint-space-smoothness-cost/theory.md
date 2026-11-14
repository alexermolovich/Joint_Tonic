# Build a Joint-Space Smoothness Cost

## Intuition

Penalizing jumps encourages nearby waypoints to agree. Each interior waypoint influences two adjacent jumps, so its gradient must collect a contribution from both sides.

## Mathematics and conventions

For $q_t\in\mathbb R^D$ in radians and nonnegative weights $w_d$ in inverse radians squared,

$$J=\sum_{t=0}^{T-2}\sum_d w_d(q_{t+1,d}-q_{t,d})^2.$$

Each edge difference $\Delta_t=q_{t+1}-q_t$ contributes $-2w\odot\Delta_t$ to row $t$ and $+2w\odot\Delta_t$ to row $t+1$. The cost is dimensionless and the gradient has inverse-radian units. Translating every waypoint by the same joint vector leaves the cost unchanged.

## Visual computation trace

| Edge | Difference | Weighted cost | Gradient contributions |
| --- | --- | --- | --- |
| 0 to 1 | 1 rad | 2 | -4, +4 |
| 1 to 2 | 2 rad | 8 | -8, +8 |

## Worked examples

1. Path `[[0.],[1.],[3.]]`, weight `[2.]` gives cost `10` and gradient `[[-4.],[-4.],[8.]]`.
2. Path `[[7.,-2.]]`, weights `[1.,3.]` gives cost zero and gradient `[[0.,0.]]`.

## Why this matters on a robot

A smooth joint path may still collide or reach the wrong target. Changing waypoint density changes this discrete objective; a time-aware formulation needs explicit sampling intervals.

## Source and prerequisites

[Primary paper](https://rll.berkeley.edu/trajopt/ijrr/). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
