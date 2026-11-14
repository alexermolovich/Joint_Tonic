# Compute Pose and Velocity Imitation Rewards

## Intuition

Motion imitation should compare physical orientations, not quaternion storage signs. Penalize squared angular disagreement and velocity disagreement separately, with scale factors that turn each error into a bounded reward.

## Mathematical mechanism

For normalized scalar-first current/reference quaternions q and h, define joint angle error $$\theta_{bj}=2\arccos(\operatorname{clip}(|q_{bj}^Th_{bj}|,0,1)).$$ Then $$r^p_b=\exp(-2\sum_j\theta_{bj}^2),\qquad r^v_b=\exp(-0.1\sum_{j,c}(\omega_{bjc}-\hat\omega_{bjc})^2).$$ B indexes synchronized states, J joints and c the three parent-local angular-velocity axes. Angles use radians and angular velocities rad/s. The coefficients have reciprocal squared units. Rewards are dimensionless. These are two DeepMimic terms; end-effector and center-of-mass terms are deliberately absent.

## Visual computation trace

| Error source | Error | Reward |
|---|---|---|
| Quaternion sign only | same rotation | pose 1 |
| One joint rotated 180 degrees | pi radians | exp(-2 pi squared) |
| One angular velocity axis | 1 rad/s | exp(-0.1) |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Identical identity rotations and angular velocities yield pose reward [1], velocity reward [1] and angle_error [[0]] for one state and joint.

## Why this matters on a robot

A robot can receive a high imitation score while violating actuator or contact constraints. Inconsistent frame conventions or quaternion signs can also create artificial motion error.

## Physical contract and limits

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

Source: [primary paper](https://arxiv.org/abs/1804.02717). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
