# Match Approximate Sensor Timestamps

## Intuition

Two sensors rarely expose frames at exactly the same instant. A bounded nearest-time association tells downstream geometry which measurements can be compared, while preserving unmatched events explicitly.

## Mathematics and physical meaning

Let $r_i$ be reference time $i$ and $q_j$ query time $j$, both in seconds. For nonempty references choose
$$i_j=\arg\min_i (|r_i-q_j|,i).$$
The pair denotes lexicographic ordering: minimize offset first, then index. Return $i_j$ only if $|r_{i_j}-q_j|\le\tau$, where $\tau\ge0$ is the tolerance in seconds. Otherwise return $-1$. This is an association, not interpolation or a one-to-one assignment.

## Visual trace

| Query | Candidates | Chosen | Within 0.2 s? |
|---|---|---|---|
| 0.1 | 0, 1 | 0 | yes |
| 0.5 | 0, 1 | 0 (tie) | no |
| 1.9 | 1, 2 | 2 | yes |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `reference=[0,1,2], queries=[0.1,0.5,1.9], tolerance=0.2` → `[0,-1,2]`. The middle sample is too far from both neighbors.
2. `reference=[0,2], queries=[1,0,2], tolerance=1` → `[0,0,1]`. The exact midpoint uses the earlier reference.

## Why this matters on a robot

A camera frame paired to a stale joint measurement can project a gripper into the wrong pixel. Keep unmatched frames visible; silently clipping to an endpoint hides timing failures. This rule does not estimate clock offset.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
