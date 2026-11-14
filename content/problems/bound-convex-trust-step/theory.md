# Bound a Sequential Convex Trust-Region Step

## Intuition

A local approximation is useful only near its linearization point. The trust radius restricts how far one update may travel, while joint limits restrict where it may end.

## Mathematics and conventions

For current joint vector $q\in\mathbb R^D$, proposed increment $p$, bounds $l,u$, and scalar radius $r$, all in radians,

$$a_d=\max(l_d-q_d,-r),\quad b_d=\min(u_d-q_d,r),\quad \Delta q_d=\operatorname{clip}(p_d,a_d,b_d).$$

The current state is already feasible, so zero belongs to every interval and the intersection cannot be empty. Return $q^+=q+\Delta q$. This is coordinatewise projection onto a box, not projection onto a Euclidean ball.

## Visual computation trace

| Joint | Remaining position interval | Trust interval | Allowed increment |
| --- | --- | --- | --- |
| 0 at 0.8 rad | [-1.8,0.2] | [-0.3,0.3] | [-0.3,0.2] |
| 1 at -0.8 rad | [-0.2,1.8] | [-0.3,0.3] | [-0.2,0.3] |

## Worked examples

1. Current `[0.8,-0.8]`, proposal `[0.5,-0.5]`, lower `[-1.,-1.]`, upper `[1.,1.]`, radius `0.3` gives step approximately `[0.2,-0.2]`, next `[1.,-1.]`, and clipped `[True,True]`.
2. Current `[0.]`, proposal `[0.1]`, limits `[-1.]` to `[1.]`, radius `0` returns step `[0.]`, next `[0.]`, clipped `[True]`.

## Why this matters on a robot

Clipping to joint limits alone can still take a step too large for the local collision model. Conversely, a small step can cross an already nearby joint bound. Re-evaluate the true scene after accepting a step.

## Source and prerequisites

[Primary paper](https://rll.berkeley.edu/trajopt/ijrr/). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
