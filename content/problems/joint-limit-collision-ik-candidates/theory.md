# Enforce Joint Limits and Collision Constraints in IK

## Intuition

IK can return several configurations for the same tool target. A valid angle range is necessary but not sufficient: the elbow or either link may intersect an obstacle while the tool itself looks clear.

## Mathematics and physical meaning

For segment endpoints $a,b\in\mathbb R^2$ and circle center $c$, project the center onto the closed segment:
$$u=\operatorname{clip}\left(\frac{(c-a)^\top(b-a)}{\|b-a\|_2^2},0,1\right),\quad d=\|a+u(b-a)-c\|_2.$$
The link collides when $d\le r+m$, where radius $r$ and margin $m$ are metres. Candidate angles $q_j$ must satisfy $l_j\le q_j\le h_j$. Rank collision-free candidates by $(\|p(q)-g\|_2,\mathrm{index})$. Links are zero-thickness line segments; margin can approximate a uniform link radius but does not model full robot geometry.

## Visual trace

| Candidate property | Decision |
|---|---|
| Any angle outside inclusive limits | reject |
| Tool clear, elbow/link crosses circle | reject |
| Link just touches inflated circle | reject |
| Both checks pass | rank by endpoint error, then index |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `lengths=[1,1], candidates=[[0,0],[pi/2,0]], joint_limits=[[-pi,pi],[-pi,pi]], obstacles=empty((0,3)), target=[2,0], margin=0` selects index0, q `[0,0]`, point `[2,0]`, error0.
2. Add obstacle `[0.5,0,0.1]`. Candidate0 crosses it, so select index1 with point approximately `[0,2]` and error `sqrt(8)`.

## Why this matters on a robot

Testing only the end effector misses link collisions. Static validity also does not certify the motion from the current pose to the chosen pose. This exercise intentionally returns a candidate decision, not a command for real hardware.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.

Each link length must be at least 1e-9 metres; smaller values raise ValueError.
