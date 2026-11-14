# Construct Motion Discriminator Features

## Intuition

A motion discriminator should recognize coordinated movement regardless of where the character stands or which way it faces. Express root velocities and endpoints in each state's own heading frame, then preserve the order of current and successor features.

## Mathematical mechanism

For yaw psi around world +y, the local-to-world heading rotation is $$R_y(\psi)=\begin{bmatrix}\cos\psi&0&\sin\psi\\0&1&0\\-\sin\psi&0&\cos\psi\end{bmatrix}.$$ World vectors become local through $R_y^T v$ and endpoint positions through $R_y^T(p_e-p_{root})$. For each joint use its parent-local rotation columns zero then one, a six-dimensional orientation code, followed by supplied parent-local angular velocity. Concatenate root linear/angular velocities, all rotation codes, all joint velocities and all endpoint positions to form $\Phi(s)\in\mathbb R^F$, where F=6+9J+3E. A transition is $[\Phi(s_t),\Phi(s_{t+1})]$ with width 2F. Each state uses its own heading. The ordering is declared here and does not imply released-checkpoint compatibility.

## Visual computation trace

| Feature block | Width | Frame and units |
|---|---|---|
| Root linear/angular velocity | 6 | heading-local m/s and rad/s |
| Joint rotation columns | 6J | parent-local dimensionless |
| Joint angular velocities | 3J | parent-local rad/s |
| Endpoints minus root | 3E | heading-local meters |
| Current then successor | 2F | same ordered schema |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

With one identity joint, zero velocities, one endpoint [1, 0, 0], root at the origin and yaw 0, a state feature is [0,0,0, 0,0,0, 1,0,0,0,1,0, 0,0,0, 1,0,0]. Identical current and successor states repeat this 18-entry vector.

## Why this matters on a robot

A robot can receive a high imitation score while violating actuator or contact constraints. Inconsistent frame conventions or quaternion signs can also create artificial motion error.

## Physical contract and limits

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

Source: [primary paper](https://arxiv.org/abs/2104.02180). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
