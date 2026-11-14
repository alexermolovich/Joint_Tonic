## Intuition: move every joint by the same fraction

A robot configuration is a list of joint angles. Imagine marking a start and an end on each of seven sliders. At the halfway sample, every slider is halfway between its own endpoints. Some joints increase, some decrease, and some stay still. They share progress along the path, not equal angle changes.

This constructs a **joint-space path**. MuJoCo then turns each configuration into positions and orientations of the robot's links. The arm's attachment point usually follows a curved path even though the joint coordinates change linearly.

## Seven coordinates, one interpolation fraction

Let $q_s,q_g\in\mathbb{R}^{7}$ denote start and goal joint vectors in radians, ordered `fr3_joint1` through `fr3_joint7`. Positive motion is a right-hand rotation around each joint's own local +z axis. The coordinates are not x, y and z positions in space.

For $N\in\{2,\ldots,101\}$ requested samples and index $k\in\{0,\ldots,N-1\}$, define the dimensionless path fraction

$$
\alpha_k=\frac{k}{N-1}.
$$

The output $Q\in\mathbb{R}^{N\times7}$ contains the joint configurations as rows:

$$
Q_{k,j}=(1-\alpha_k)q_{s,j}+\alpha_kq_{g,j},\qquad j=0,\ldots,6.
$$

At $k=0$, $\alpha_k=0$ and the output is exactly the start. At $k=N-1$, the fraction is one and the output is the goal. Using $N$ in the denominator misses the goal.

### Shape trace and text diagram

| Stage | Shape | Meaning |
|---|---|---|
| Start and goal | `(7,)` each | Two configurations, radians |
| Fractions | `(N,1)` | One fraction per row, dimensionless |
| Broadcast mixture | `(N,7)` | Seven joint angles per sample |
| MuJoCo forward kinematics | One attachment pose per row | Position in meters and dimensionless rotation |

```text
start angles (7,) ----\
                       >-- shared fractions (N,1) --> joint rows (N,7)
goal angles (7,) -----/                                  |
                                                         v
                                  MuJoCo attachment pose in world/base
```

This diagram's table is its text alternative. The simulator also exposes numerical joint values and attachment pose; manual stepping does not require animation.

## Work through the midpoint

Take the example's fourth joint (column 3): $q_{s,3}=-1.0$ rad and $q_{g,3}=-1.4$ rad. With $N=3$, the fractions are $0,0.5,1$. At the middle row:

$$
Q_{1,3}=0.5(-1.0)+0.5(-1.4)=-1.2\;\mathrm{rad}.
$$

The sixth joint changes from 1.0 to 1.4 rad and reaches 1.2 rad at that same row. The full row is `[0.2, 0.1, -0.1, -1.2, 0.3, 1.2, -0.2]`. These numbers are all angles; they do not say that the tool moved 0.2 meters.

## Joint limits and what they do not guarantee

For joint $j$, let $\ell_j,u_j$ be the minimum and maximum model angles from the problem's table, in radians. If both endpoints satisfy $\ell_j\leq q_{s,j},q_{g,j}\leq u_j$, then every convex mixture with $0\leq\alpha\leq1$ remains in that interval:

$$
\ell_j\leq (1-\alpha)q_{s,j}+\alpha q_{g,j}\leq u_j.
$$

This is why the problem validates endpoints and uses the unwrapped bounded coordinates directly. Modulo-$2\pi$ wrapping could introduce a different path or a discontinuity. Position limits alone do **not** prove that an intermediate robot shape avoids the floor, itself, or an obstacle.

## Why the attachment point moves differently

The simulator uses the pinned FR3 link transforms. Write its forward-kinematic map as

$$
{}^{W}T_A(q)=\begin{bmatrix}{}^{W}R_A(q)&{}^{W}p_A(q)\\0&1\end{bmatrix}\in\mathbb{R}^{4\times4}.
$$

$W$ is the fixed world/base frame with +z up; $A$ is the model's `attachment_site` at the arm flange, without a gripper. The vector ${}^{W}p_A\in\mathbb{R}^3$ is measured in meters and ${}^{W}R_A\in\mathbb{R}^{3\times3}$ is a dimensionless rotation matrix. The transform composes the model's fixed link offsets with rotations depending on all seven angles. In general,

$$
{}^{W}p_A((1-\alpha)q_s+\alpha q_g)\ne(1-\alpha){}^{W}p_A(q_s)+\alpha{}^{W}p_A(q_g).
$$

You implement the configuration interpolation, not this forward-kinematic map. MuJoCo evaluates the map for the displayed poses after assigning `qpos`; this is kinematic replay, not a dynamics rollout under motor torque.

## Why this matters on a robot

A waypoint generator is a useful first component in trajectory tools, replay inspection, and controller tests. It establishes explicit joint ordering and endpoints before velocity constraints or obstacle reasoning are introduced.

This task has no physical duration. If a later system assigns duration $T>0$ seconds to the continuous path, its interior velocity would be $(q_g-q_s)/T$ rad/s. Starting or stopping that constant velocity abruptly creates acceleration discontinuities. A real controller needs time parameterization and validated velocity, acceleration, torque, and collision constraints. Increasing the number of display samples does not make those constraints true.

Common failures include swapping joint order, supplying degrees instead of radians, treating the two positive-only/negative-only joint ranges as symmetric, omitting the final sample, or mistaking a valid rendered pose for a safe physical motion. The simulator reports visual/kinematic evidence; numerical grading and robot safety are separate concerns.

## Sources and next steps

- [Pinned official Menagerie FR3 model](https://github.com/google-deepmind/mujoco_menagerie/tree/98a70c569c4c1b6da467a20012f766ee1f8dc521/franka_fr3): model identity, joint ranges and attachment frame. This is FR3, not the older Panda model.
- [Franka joint specifications](https://frankarobotics.github.io/docs/robot_specifications.html): hardware limits depend on model/system version; this task's exact table is the pinned simulator contract.
- [MuJoCo forward computation](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html#mj-forward): simulator-side state evaluation.
- Related practice: [Compose and Invert Coordinate Transforms](/problems/compose-frame-transforms), then [Planar Two-Link IK](/problems/planar-two-link-ik). Neither is required to implement this interpolation task.
