# Map Robot-Specific Data into a Shared Episode Schema

## Intuition

A shared field name is useful only when it retains meaning. A value25 can mean centimetres, millimetres or radians. This mapper performs a deliberately narrow conversion and carries provenance along so a later learner can trace every row back to its dataset and robot.

## A declared channel map

Let $X\in\mathbb R^{T\times S}$ hold T source samples and S scalar channels. Target channel j selects source column $k(j)$ and has compatible scale factors $a_j^{\mathrm{src}},a_j^{\mathrm{dst}}$ to a shared family base. Output $Y\in\mathbb R^{T\times D}$ is

$$
Y_{t,j}=X_{t,k(j)}\,\frac{a_j^{\mathrm{src}}}{a_j^{\mathrm{dst}}}.
$$

Length uses metres as base, angle uses radians and unitless stays unitless. For degrees, $a=\pi/180$. The original frame and position/delta control mode remain unchanged. Nanosecond timestamps are exact integers copied alongside samples, not rescaled floats.

## Visual: semantic column mapping

| Source channel/value | Source unit | Target column/unit | Computed value |
|---|---|---|---:|
| x=25 | cm | first, m | 0.25 |
| yaw=90 | deg | second, rad | pi/2 |

This original static mapping table is also the text alternative. The sample remains at timestamp100ns in frame base and mode delta.

## What conversion cannot establish

Reordering Cartesian x,y,z values into positions named joint1,joint2,joint3 would be a semantic error even if shapes matched. This function requires matching source names and compatible unit families. It does not solve inverse kinematics or reconcile different action conventions.

## Why this matters on a robot

Dropping dataset version or control mode makes a mixed training batch ambiguous. A policy trained on absolute positions and then decoded as deltas can command large unintended motion. Preserve identity and reject unsupported conversions instead of guessing.

## Questions

1. Why is centimetres-to-radians rejected?
2. Why retain integer timestamps even after converting float signal values?

## Sources and prerequisites

Open X-Embodiment motivates shared data interfaces that preserve robot-specific meaning. This restricted scalar position/delta mapper and unit table are original teaching choices; they do not reproduce every source dataset transform or make embodiments interchangeable. [Primary source](https://arxiv.org/abs/2310.08864), SectionIV-A data format consolidation. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

