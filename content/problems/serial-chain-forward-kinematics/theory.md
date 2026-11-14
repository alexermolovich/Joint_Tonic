# Compute Forward Kinematics for a Serial Chain

## Intuition

Every link inherits all upstream joint rotations. The elbow angle changes the direction of the forearm relative to the upper arm, not relative to the room.

## Mathematics and physical meaning

For link index $i=1,\ldots,N$, let $L_i>0$ be length in metres and $q_i$ the relative angle in radians. Absolute orientation is $\theta_i=\sum_{k=1}^i q_k$. Starting at $p_0=(0,0)$,
$$p_i=p_{i-1}+L_i[\cos\theta_i,\sin\theta_i]^\top.$$
With final $p_N=(x,y)$, the tool-to-base transform is
$$T=\begin{bmatrix}\cos\theta_N&-\sin\theta_N&x\\\sin\theta_N&\cos\theta_N&y\\0&0&1\end{bmatrix}.$$
The local operation is rotation followed by translation along the rotated x-axis. Changing this order describes a different robot.

## Visual trace

| Link, lengths [1,0.5], q=[pi/2,-pi/2] | Absolute angle | Distal endpoint (m) |
|---|---|---|
| Base | 0 | [0,0] |
| 1 | pi/2 | [0,1] |
| 2 | 0 | [0.5,1] |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `lengths=[1,0.5], q=[pi/2,-pi/2]` → origins `[[0,0],[0,1],[0.5,1]]`, tool pose `[[1,0,0.5],[0,1,1],[0,0,1]]` up to roundoff.
2. `lengths=[2], q=[0]` → origins `[[0,0],[2,0]]`, tool pose `[[1,0,2],[0,1,0],[0,0,1]]`.

## Why this matters on a robot

The intermediate origins are needed to check links against obstacles; the tool pose alone cannot locate the elbow. Wrong local versus absolute angle conventions can produce a plausible endpoint for an entirely different arm.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
