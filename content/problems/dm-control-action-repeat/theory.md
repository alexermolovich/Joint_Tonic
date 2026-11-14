# Implement Action Repeat Correctly

## Intuition

Holding an action for several simulator transitions changes the control period. To combine those transitions, carry a running discount product and stop at the first episode boundary. A zero bootstrap discount changes the weighted reward sum but is not itself a LAST marker.

## Mathematics and physical contract

For consumed transition rewards $r_i$ and discounts $d_i$, let $K$ be the repeat limit or the first LAST position plus one, whichever occurs first. Define prefix weight $w_0=1$ and $w_i=\prod_{j<i}d_j$. Then
$$R=\sum_{i=0}^{K-1}w_i r_i,\qquad D=\prod_{i=0}^{K-1}d_i.$$
Rewards have the supplied task reward unit; discounts and $w_i$ are dimensionless. There is no extra agent discount in this contract. If each underlying transition spans $\Delta t$, an uninterrupted repeat of $K$ transitions spans $K\Delta t$; the function receives evidence rather than timestamps or physical actions.

## Worked pipeline and shape trace

```text
i  reward  discount  prefix  weighted reward  LAST
0    1       0.5       1          1          False
1    2       1         0.5        1          True
2   99       1         --         --         ignored
R=2, D=0.5, steps=2, last=True
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

Aggregating past LAST can attach the next episode to the current action. Discarding nonzero final discounts at a time limit changes downstream learning targets. This task cannot establish that a real actuator held the intended command.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2018-deepmind-control-suite](https://github.com/google-deepmind/dm_env/blob/master/dm_env/_environment.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
