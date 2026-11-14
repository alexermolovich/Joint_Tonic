# Compute a Signed-Distance Collision Cost

## Intuition

Signed separation distinguishes outside, touching, and overlapping spheres. A safety-margin cost can be active before actual contact, while a contact flag remains meaningful even when a zero-margin hinge is zero.

## Mathematics and conventions

For robot sphere $i$ in batch $b$ and obstacle $k$, centers $c_{bi},o_k\in\mathbb R^3$ and radii $r_i,R_k$ are in meters:

$$d_{bik}=\|c_{bi}-o_k\|_2-r_i-R_k,\qquad J_b=\sum_{i,k}\max(0,m-d_{bik})^2.$$

Margin $m$ and clearance have meter units; $J$ has squared-meter units. The collision indicator is $\mathbf1[\min_{i,k}d_{bik}\le0]$. No gradient is requested, avoiding an unstated direction convention at coincident sphere centers.

## Visual computation trace

| Center distance | Radius sum | Clearance | Contact? |
| --- | --- | --- | --- |
| 3 m | 2 m | +1 m | no |
| 2 m | 2 m | 0 m | yes |
| 1 m | 2 m | -1 m | yes |

## Worked examples

1. One robot sphere centered at `(0,0,0)` meters with radius 1, one obstacle at `(3,0,0)` radius 1, margin 2: clearance 1 m, cost 1 m², collision False.
2. Move the obstacle to `(2,0,0)` and set margin0: clearance zero, cost zero, collision True because the spheres touch.

## Why this matters on a robot

Sphere approximations are only as reliable as their coverage of the robot and obstacle geometry. A low sum cost can hide a single collision, so inspect the explicit minimum clearance and contact flag.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2310.17274). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
