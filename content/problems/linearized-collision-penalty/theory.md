# Linearize a Signed-Distance Collision Penalty

## Intuition

A local clearance Jacobian predicts how a small joint movement changes obstacle separation. The hinge responds only to predicted pairs inside the requested margin; gradients from satisfied pairs do not contribute.

## Mathematics and conventions

At current joint vector $\bar q\in\mathbb R^D$, supplied clearances $d\in\mathbb R^N$ and Jacobian $J\in\mathbb R^{N\times D}$ define

$$\tilde d=d+J\Delta q,\qquad L=\sum_i\max(0,m-\tilde d_i),\qquad g=-\sum_{i:\tilde d_i<m}J_{i,:}.$$

$\Delta q$ is in radians, $d,m,\tilde d,L$ in meters, and each gradient component in meters/radian. At equality a hinge has multiple valid subgradients; this contract chooses zero. Large steps can invalidate the linear approximation even when its predicted penalty falls.

## Visual computation trace

| Pair | Current clearance | Predicted clearance | Hinge at 0.05 m |
| --- | --- | --- | --- |
| 0 | 0.02 m | 0.03 m | 0.02 m |
| 1 | 0.08 m | 0.07 m | 0 |

## Worked examples

1. Distances `[0.02,0.08]`, Jacobian `[[1.],[-1.]]`, step `[0.01]`, margin `0.05`: predicted `[0.03,0.07]`, hinge `[0.02,0.]`, cost `0.02`, gradient `[-1.]`.
2. Distance `[0.05]`, Jacobian `[[2.]]`, step `[0.]`, margin `0.05`: hinge and cost zero, chosen gradient `[0.]` at the kink.

## Why this matters on a robot

A local optimizer must recheck actual collision geometry after updating the configuration. A wrong Jacobian sign can confidently move the robot toward an obstacle while reporting predicted improvement.

## Source and prerequisites

[Primary paper](https://rll.berkeley.edu/trajopt/ijrr/). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
