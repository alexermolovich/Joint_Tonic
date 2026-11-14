# Push Robot State into a Task Space

## Intuition

A Jacobian converts a small joint displacement into a task displacement. The same linear map converts instantaneous joint velocity, provided it is evaluated at the current configuration.

## Mathematics and conventions

For task map $x=\psi(q)$, with $q\in\mathbb R^D$ in radians and $x\in\mathbb R^T$ in meters, its supplied Jacobian is $J=\partial\psi/\partial q\in\mathbb R^{T\times D}$.

$$\dot x=J\dot q,\qquad \dot x_i=\sum_{j=1}^D J_{ij}\dot q_j.$$

The units are $(\mathrm{m/rad})(\mathrm{rad/s})=\mathrm{m/s}$. Position is already evaluated and is copied unchanged. The velocity map is local in configuration and time; this operation does not update the robot state.

## Visual computation trace

| Task row | Joint contributions for velocity `[2,-1]` | Result |
| --- | --- | --- |
| `[1,2]` | `1*2 + 2*(-1)` | 0 m/s |
| `[0,1]` | `0*2 + 1*(-1)` | -1 m/s |

## Worked examples

1. Position `[3.,4.]`, Jacobian `[[1.,2.],[0.,1.]]`, joint velocity `[2.,-1.]` give position `[3.,4.]` and task velocity `[0.,-1.]` m/s.
2. Position `[1.]`, Jacobian `[[2.,3.]]`, joint velocity `[0.,0.]` give position `[1.]` and velocity `[0.]`, both in fresh arrays.

## Why this matters on a robot

A stale Jacobian can predict the wrong end-effector velocity even when all shapes match. Mixing a Jacobian in one task frame with a position expressed in another breaks policy composition.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1811.07049). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
