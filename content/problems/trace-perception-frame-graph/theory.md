# Trace Frames Through a Robot Perception Graph

## Intuition

A perception point might travel from camera coordinates through a wrist frame into the robot base. A frame graph records those relationships so composition order is explicit instead of being guessed from matrix shapes.

## Mathematics and physical meaning

An edge $(a,b,T_{ab})$ means $p_a=T_{ab}p_b$ in homogeneous coordinates. For a path from source $s$ through $b$ to target $a$,
$$T_{as}=T_{ab}T_{bs}.$$
Reverse an edge with $T_{ba}=\begin{bmatrix}R_{ab}^\top&-R_{ab}^\top t_{ab}\\0&1\end{bmatrix}$. A forest gives at most one path; rejecting cycles avoids silently choosing among inconsistent calibrations. Translation is metres and rotations use one common right-handed convention.

## Visual trace

| Path operation | Matrix applied | Running map |
|---|---|---|
| camera -> wrist | T_wrist_camera | camera to wrist |
| wrist -> base | T_base_wrist | T_base_wrist @ T_wrist_camera |
| base -> camera | inverse of full product | base to camera |

This static table is also the text alternative; no animation is required.

## Worked examples

1. Let T_base_wrist translate `[1,0,0]` and T_wrist_camera translate `[0,2,0]`. Resolving source="camera", target="base" returns translation `[1,2,0]` with identity rotation.
2. Reversing those query frames returns translation `[-1,-2,0]`. A known frame to itself returns identity.

## Why this matters on a robot

Reversing one transform can place a detected object on the wrong side of a robot. Tree validation catches structural ambiguity, but a correctly shaped and connected graph can still contain a physically wrong calibration.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
