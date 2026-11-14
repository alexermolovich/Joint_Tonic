# Construct Relative Pose Measurements from Local Odometry

## Intuition

An odometry trajectory describes poses in a shared local frame. A graph edge should express motion in its starting body frame, so global translation differences must first be rotated back into that frame.

## Mathematics and conventions

Let $T_i=[R_i,p_i;0,1]\in\mathbb R^{4\times4}$ map body frame $i$ into the local world. For a supplied temporal edge $(i,j)$, $i<j$, compute
$$R_{ij}=R_i^\top R_j,\qquad p_{ij}=R_i^\top(p_j-p_i),\qquad T_{ij}=T_i^{-1}T_j.$$
The edge maps coordinates from body $j$ into body $i$. Positions and $p_{ij}\in\mathbb R^3$ are meters. With timestamps $t_i,t_j$ in seconds,
$$\Delta t_{ij}=t_j-t_i,\qquad s_{ij}=\frac{\|p_{ij}\|_2}{\Delta t_{ij}}.$$
The scalar $s_{ij}$ is meters per second, measuring endpoint displacement divided by elapsed time. It need not equal traveled distance divided by time. Preserve the supplied edge order, including repeated edges; no sensor synchronization is inferred.

## Visual computation trace

```text
body-j point -> Tj -> local-world point -> inverse(Ti) -> body-i point
poses(N,4,4), edges(E,2) -> edge transforms(E,4,4)
timestamps(N) -> positive durations(E) -> chord speeds(E)
```

## Worked examples

1. Identity rotations, local positions x=0 and x=2 meters at times 0 and 2 seconds, edge [0,1]: output translation [2,0,0], duration 2, chord speed 1 m/s.
2. First pose rotates 90 degrees about z at the origin; second has identity rotation and world position [1,0,0]. The relative rotation is -90 degrees about z and translation [0,-1,0].

## Why this matters on a robot

Using a world displacement directly as a body-frame measurement rotates the constraint incorrectly whenever the robot turns. A long curved route can have small chord speed; this diagnostic is not an actuator velocity bound.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1901.03642). [compose-frame-transforms](/problems/compose-frame-transforms)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
