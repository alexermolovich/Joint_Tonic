# A target can have several joint explanations

## Intuition

Forward kinematics maps joint angles to a tool position. Inverse kinematics reverses that question. A two-link planar arm often has two possible elbows, so a useful function must declare which branch it returns.

Let $L_1,L_2$ be positive lengths in meters, $(x,y)$ the target in the fixed base frame, and $q_1,q_2$ shoulder and relative elbow angles in radians. Both rotate counterclockwise about +z.

## Reachability before angles

The distance $r=\sqrt{x^2+y^2}$ must lie in an annulus:

$$
|L_1-L_2|\le r\le L_1+L_2.
$$

Outside it, a link would need to stretch or shrink. The exercise allows a 1e-9 m boundary tolerance; that is numerical policy, not mechanical compliance.

Using the triangle formed by the links and target:

$$
c_2=\frac{r^2-L_1^2-L_2^2}{2L_1L_2},\qquad q_2=\arccos(\operatorname{clip}(c_2,-1,1)),
$$

$$
q_1=\operatorname{atan2}(y,x)-
\operatorname{atan2}(L_2\sin q_2,L_1+L_2\cos q_2).
$$

The arccos choice fixes the elbow branch. Clamp only after rejecting truly unreachable targets. Normalize q1 to [-pi,pi) so equivalent angle wraps have one declared representation.

The exercise bounds link lengths to 1 mm through 1000 m and their ratio to 1000. Extreme ratios magnify cancellation in the cosine calculation; accepting them would promise accuracy that this elementary float64 solver cannot reliably deliver.

## Visual: verify the links endpoint by endpoint

| Point for unit links | x (m) | y (m) | Construction |
|---|---:|---:|---|
| Shoulder | 0 | 0 | Base origin |
| Elbow | 1 | 0 | q1=0 |
| Tool | 1 | 1 | q1+q2=pi/2 |

The table is a static arm diagram and text alternative: move one meter right, then one meter up. For target (1,1), c2=0 and q2=pi/2; both bearing and internal offset are pi/4, so q1=0.

The independent forward check is

$$
\begin{bmatrix}x\\y\end{bmatrix}
=\begin{bmatrix}
L_1\cos q_1+L_2\cos(q_1+q_2)\\
L_1\sin q_1+L_2\sin(q_1+q_2)
\end{bmatrix}.
$$

## Singular geometry and robot failures

At full extension or folding, sin(q2) is zero: some tiny tool displacements demand large joint changes. The declared singular flag uses abs(sin(q2))<=1e-9. Equal links folded to the origin have infinitely many shoulder choices; choosing zero makes the contract deterministic.

A valid geometric answer can collide with an obstacle or exceed a joint limit. This task is not a motion planner, and a branch chosen independently each frame can jump discontinuously. MuJoCo visualization and constraint-aware IK belong to later components.

## Check your understanding

- Can clipping c2 make every target valid? It can hide impossible targets; check reachability first.
- Is q2 an absolute orientation? No; link2's absolute orientation is q1+q2.

## Source

See [Modern Robotics, chapter6](https://hades.mech.northwestern.edu/images/7/7e/MR-2up-v2.pdf) for planar IK geometry. These examples, validation limits and deterministic return contract are original.
