# Interpolate a Reference Motion Pose

## Intuition

A reference motion is sampled at discrete times, while a controller may request an intermediate pose. Interpolate translation linearly and rotation along its shortest spherical arc, remembering that opposite quaternion signs represent the same orientation.

## Mathematical mechanism

For neighboring timestamps $t_i,t_{i+1}$ and a clamped query t, let $$u=\frac{t-t_i}{t_{i+1}-t_i},\qquad p(t)=(1-u)p_i+up_{i+1}.$$ The positions p are world-frame meters. Normalize scalar-first joint quaternions q and h; negate h when $q^Th<0$. With $\theta=\arccos(\operatorname{clip}(q^Th,0,1))$, $$q(t)=\frac{\sin((1-u)\theta)}{\sin\theta}q+\frac{\sin(u\theta)}{\sin\theta}h.$$ For dot products above 0.9995 use normalized linear interpolation to avoid division near zero. Normalize the final quaternion too. Quaternions are parent-relative joint orientations; this interpolation supplies kinematics and does not enforce dynamic feasibility.

## Visual computation trace

| Query time | Segment | Fraction | Root x for endpoints 0 and 2 m |
|---|---|---|---|
| 0 s | 0 to 2 s | 0 | 0 m |
| 1 s | 0 to 2 s | 0.5 | 1 m |
| 3 s | clamp to end | 1 | 2 m |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Times [0, 2], root positions [[0, 0, 0], [2, 0, 0]], identity joint quaternions and query [1] yield root position [[1, 0, 0]], identity orientation, interval [0] and alpha [0.5].

## Why this matters on a robot

A robot can receive a high imitation score while violating actuator or contact constraints. Inconsistent frame conventions or quaternion signs can also create artificial motion error.

## Physical contract and limits

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

Source: [primary paper](https://arxiv.org/abs/1804.02717). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
