# Joint motion becomes tool motion through a lever arm

## Intuition

A revolute joint makes a distant point move along a circle. The farther the tool is from that axis, the faster it moves for the same angular speed. A prismatic joint simply slides everything downstream along its axis. The geometric Jacobian collects those instantaneous effects into one column per joint.

Every input here is expressed in the same base frame at one robot configuration. Let $o_i$ be joint i's origin in meters, $z_i$ its unit axis, and $p$ the tool origin in meters. Let $\dot q_i$ be the joint rate.

## Constructing a column

For a revolute joint, the tool's lever arm is $p-o_i$. Its induced linear velocity is perpendicular to both the axis and lever arm:

$$
J_i=
\begin{bmatrix}
z_i\times(p-o_i)\\
z_i
\end{bmatrix}.
$$

For a prismatic joint, sliding changes position without changing orientation:

$$
J_i=
\begin{bmatrix}
z_i\\
0
\end{bmatrix}.
$$

Stacking these columns gives $J\in\mathbb R^{6\times N}$. Under this lesson's convention:

$$
\begin{bmatrix}v\\\omega\end{bmatrix}=J\dot q.
$$

The top three rows describe tool-origin linear velocity in m/s; the bottom rows describe angular velocity in rad/s. Revolute and prismatic columns therefore have different physical unit relationships. Record the joint types instead of treating all rates as interchangeable numbers.

## Worked robot example

A +z revolute axis through the base acts on a tool at $(2,0,0)$. Its lever arm is two meters along x, so the linear column is $(0,2,0)$ and the angular column is $(0,0,1)$. At 0.5 rad/s, the tool initially moves at 1 m/s along +y and rotates at 0.5 rad/s.

## Visual and assessment plan

The robot view will draw each joint axis, lever arm, and induced velocity arrow. Selecting a column isolates one joint's contribution. A numerical table exposes all six components and a small forward-kinematics step checks the direction. Linearization predicts only a short displacement; it is not an exact finite-motion formula.

## Why it matters and what can fail

Jacobians connect task-space control, force reasoning, and numerical IK. Using a joint's local axis with a base-frame lever arm produces a plausible but physically wrong cross product. Swapping angular-first and linear-first conventions causes another silent interface failure. Singular configurations can make different joint columns dependent; constructing J remains valid even when a later inverse is ill-conditioned. This task intentionally stops before solving that inverse problem.
