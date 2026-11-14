# Every link inherits the turns before it

## Intuition

A shoulder rotation moves the entire arm beyond the shoulder. An elbow rotation moves only the links after the elbow. Forward kinematics turns a complete joint configuration into a set of link poses by accumulating those local changes.

This lesson uses a planar serial chain. Joint angle $q_i$ is relative to the preceding link, measured in radians about +z. Link length $L_i$ is a positive distance in meters along the link's rotated +x axis. The base frame is fixed at $(0,0)$.

## The chain convention

Let $\theta_i$ be link i's absolute orientation in the base frame:

$$
\theta_i=\sum_{k=1}^{i}q_k.
$$

Let $p_0=(0,0)$ and $p_i$ be the distal endpoint of link i. Each displacement must be expressed using the accumulated orientation:

$$
p_i=p_{i-1}+L_i
\begin{bmatrix}\cos\theta_i\\\sin\theta_i\end{bmatrix}.
$$

A single local transform rotates by $q_i$ and then translates along the new x-axis. In homogeneous coordinates, this is $A_i=R(q_i)T_x(L_i)$, and the tool pose is the ordered product $A_1A_2\cdots A_N$. Reversing rotation and translation describes a different mechanism.

The output includes intermediate origins because the end-effector pose alone cannot show where every link occupies space. Later collision checks and geometric Jacobians need those origins.

## Worked robot configuration

Take links of length 1 and 0.5 meters. With $q=(\pi/2,-\pi/2)$, the first link points along base +y. Its endpoint is $(0,1)$. The second link's absolute orientation is zero, so it points along base +x and ends at $(0.5,1)$. The tool orientation is also zero. Treating the second angle as an absolute orientation would instead point it down.

## Visual and assessment plan

A MuJoCo side view will label each joint origin and draw local axes. Moving one joint highlights which downstream poses change. A companion table lists cumulative angle, local displacement, and endpoint. Numerical checks compare link lengths and the agreement between the final endpoint and tool transform, rather than grading rendered pixels.

## Why it matters and what can fail

Forward kinematics is the model used to verify an inverse-kinematics solution and to locate collision geometry. A convention mismatch between an asset and solver can put every link in the wrong place even when the final target looks close. Pin link order, joint zero positions, units, and asset version together. This planar problem teaches composition; it does not yet model 3D screw axes, joint elasticity, dynamics, or actuator tracking error.
