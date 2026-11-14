# Compute a Geometric Jacobian from Joint Axes

## Intuition

A rotating joint moves a distant tool perpendicular to its lever arm. A sliding joint moves the tool directly along its axis. Placing these effects in columns makes simultaneous joint motion a matrix-vector product.

## Mathematics and physical meaning

For joint origin $o_i$ and tool position $p$ in metres, and unit base-frame axis $z_i$, a revolute joint has
$$J_i=\begin{bmatrix}z_i\times(p-o_i)\\z_i\end{bmatrix}.$$
A prismatic joint has $J_i=[z_i^\top,0,0,0]^\top$. Stack the columns into $J\in\mathbb R^{6\times N}$, giving $[v^\top,\omega^\top]^\top=J\dot q$. Linear velocity $v$ is m/s and angular velocity $\omega$ is rad/s. Revolute rates are rad/s; prismatic rates are m/s. This is a geometric Jacobian at the tool origin, not an angular-first spatial-twist convention.

## Visual trace

| Joint | Axis | Lever arm | Linear column | Angular column |
|---|---|---|---|---|
| Revolute | [0,0,1] | [2,0,0] | [0,2,0] | [0,0,1] |
| Prismatic | [1,0,0] | irrelevant | [1,0,0] | [0,0,0] |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `origins=[[0,0,0]], axes=[[0,0,1]], joint_types=["R"], tool=[2,0,0]` → column `[0,2,0,0,0,1]`.
2. Same origin/tool with `axes=[[1,0,0]], joint_types=["P"]` → column `[1,0,0,0,0,0]`.

## Why this matters on a robot

Local-frame axes combined with a base-frame tool position produce a wrong cross product even when every shape passes. Constructing the Jacobian remains valid at singularities; inverting it is a separate numerical problem.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
