# Enforce Velocity and Acceleration Limits

## Intuition

A target jump should not instantly become an arbitrarily fast motion. Limiting speed alone still allows abrupt velocity changes. Intersecting the speed and acceleration intervals gives a feasible next velocity for each joint.

## Mathematics and physical meaning

At step $k$, let current joint position be $q_k$, previous velocity $v_{k-1}$, requested next position $g_k$, and interval $\Delta t>0$. For each joint, define
$$v_k^*=\frac{g_k-q_k}{\Delta t},\quad l_k=\max(-v_{\max},v_{k-1}-a_{\max}\Delta t),\quad h_k=\min(v_{\max},v_{k-1}+a_{\max}\Delta t).$$
Then $v_k=\operatorname{clip}(v_k^*,l_k,h_k)$ and $q_{k+1}=q_k+v_k\Delta t$. Velocities have rad/s units and accelerations rad/s². Valid initial velocity guarantees the intersection is nonempty. This greedy projection does not anticipate future targets or minimize a global trajectory objective.

## Visual trace

| Step, target=10 rad, dt=1 s | Previous v | Feasible next v with vmax=2,amax=1 | Next position |
|---|---|---|---|
| 0 | 0 | [-1,1] -> 1 | 1 |
| 1 | 1 | [0,2] -> 2 | 3 |
| 2 | 2 | [1,2] -> 2 | 5 |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `initial_position=[0], initial_velocity=[0], targets=[[10],[10],[10]], dt=1, max_velocity=[2], max_acceleration=[1]` → positions `[[1],[3],[5]]`, velocities `[[1],[2],[2]]`.
2. `initial_position=[0], initial_velocity=[2], targets=[[-10]], dt=1, max_velocity=[2], max_acceleration=[1]` → position `[[1]]`, velocity `[[1]]`; braking cannot reverse velocity instantly.

## Why this matters on a robot

Even when the target is behind the arm, bounded braking may require continuing forward briefly. A collision-aware planner must account for that stopping motion. This exercise is a command shaper, not an emergency-stop or hardware safety controller.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.

dt must be at least 1e-9 seconds; smaller values raise ValueError.
