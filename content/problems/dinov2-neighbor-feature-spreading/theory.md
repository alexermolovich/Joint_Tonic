# Implement Nearest-Neighbor Feature-Spreading Regularization

## Intuition

A representation can collapse when many images receive nearly identical features. A nearest-neighbor spreading penalty discourages crowding on the unit sphere. It is possible for this loss to be negative: distances greater than one have positive logarithms.

## Mathematics and physical meaning

Rows $x_i\in\mathbb R^D$ are dimensionless frozen features, with $N\ge2$ and nonzero norm. Normalize $z_i=x_i/\|x_i\|_2$. Exclude the diagonal when selecting the nearest other row:
$$n_i=\underset{j\ne i}{\operatorname{argmin}}\|z_i-z_j\|_2,\qquad d_i=\|z_i-z_{n_i}\|_2.$$
Ties choose the smallest original row index. The explicitly clamped teaching objective is
$$L=-\frac1N\sum_i\log(\max(d_i,\epsilon)).$$
Return unclamped distances $(N,)$ and integer neighbors $(N,)$, plus the scalar loss. The clamp affects only the logarithm; duplicates correctly return distance zero. Unit vectors give distances in $[0,2]$. This is a KoLeo-style component, not a claim to duplicate every released numerical detail or perform encoder optimization.

## Visual trace

| Features | Neighbors | Distances | Loss |
|---|---|---|---|
| `[1,0]`, `[-1,0]` | `[1,0]` | `[2,2]` | `-log(2)` |
| Three identical unit vectors | `[1,0,0]` | `[0,0,0]` | `-log(epsilon)` |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** Features `[[1, 0],[-1, 0]]` with epsilon `.01` return distances `[2, 2]`, neighbors `[1, 0]`, and loss `-log(2)`.

**Example 2.** Three identical nonzero feature rows return distances `[0, 0, 0]`, neighbors `[1, 0, 0]`, and loss `-log(epsilon)`. The diagonal is excluded even when other rows are duplicates.

## Why this matters on a robot

Reusable visual features should distinguish different scenes before a robot policy consumes them. Accidentally selecting each feature as its own neighbor makes every distance zero and destroys the intended learning signal.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2304.07193). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
