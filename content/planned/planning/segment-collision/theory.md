# Check a Motion Segment Against Inflated Obstacles: theory

## Intuition

Checking only a motion's start and end can miss a collision in between. A segment validator asks whether any intermediate robot-center position enters an obstacle. Clearance can be included before testing by enlarging obstacles, so the center stays farther from their surfaces.

## Parameterize the proposed motion

Let $a,b\in\mathbb R^2$ be world positions in meters. Every point on the segment is

$$
p(t)=a+t(b-a),\qquad 0\leq t\leq1.
$$

The parameter $t$ is a fraction of the segment, not elapsed seconds. No velocity is implied unless a separate trajectory supplies timing. A zero-length segment has $a=b$ and reduces to checking one location.

For an obstacle with lower corner $l$ and upper corner $u$, clearance $d\geq0$ creates expanded bounds $l-d$ and $u+d$ coordinate-wise. This is exact for an axis-aligned square center envelope and conservative for a circular robot near box corners.

## Intersect allowed parameter intervals

For each coordinate axis, solve the condition

$$
l_i-d\leq a_i+t(b_i-a_i)\leq u_i+d.
$$

A nonzero direction component gives a lower and upper allowed value of $t$; exchange them when direction is negative. Intersect the x interval, y interval, and $[0,1]$. A nonempty intersection means collision. With zero direction on an axis, the fixed coordinate must already lie within that axis's closed bounds.

The first intersecting parameter is the entry point. Compare it across obstacles and keep the smallest one, with original index as the tie breaker. Closed intervals deliberately count contact as collision.

## Worked obstacle example

Move from $(0,0)$ to $(4,0)$ past box $[2,-1,3,1]$, with zero clearance. The x constraint permits $t\in[0.5,0.75]$ and y is always inside. Collision starts at $t=0.5$, even though both motion endpoints are outside the box.

At height y=2, the same segment clears the box with zero margin. A 1 m clearance expands its top boundary to y=2, so contact now counts as blocked.

## Visual explanation

Show the original box, expanded box, segment, and highlighted entry point. A table displays per-axis parameter intervals and their intersection. This explains near-boundary outcomes without requiring precise pointer placement.

## Robot relevance and failure modes

Sparse sampling can step over a thin obstacle. Ignoring a zero direction causes divide-by-zero errors. Treating box corners as an exact circular inflation overstates the geometric model. This component provides a deterministic validity check that can be reused by classical or learned planners.

