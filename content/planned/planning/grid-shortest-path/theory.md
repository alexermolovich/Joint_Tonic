# Plan a Shortest Route on an Occupancy Grid: theory

## Intuition

A grid map turns free space into a graph. Each free cell is a possible robot location, and an edge represents one permitted move. A route is valid only if every visited cell is free and every consecutive pair follows the motion model. A geometric line to the goal is not enough when obstacles block it.

## Cost and search guidance

Let a state be cell $(r,c)$ and the goal be $(r_g,c_g)$. Four-neighbor moves change one coordinate by one. Their Manhattan separation is

$$
h(r,c)=|r-r_g|+|c-c_g|.
$$

The heuristic counts steps, not meters. It never overestimates the required remaining moves under this motion model because obstacles can force detours but cannot eliminate the coordinate displacement.

If $g(n)$ is the best discovered step count to state $n$, A* orders candidates by

$$
f(n)=g(n)+h(n),\qquad C_{\mathrm{meters}}=g(\mathrm{goal})\,s,
$$

where $s>0$ is cell size in meters. Keeping all search priorities in steps avoids mixing coordinate count with physical distance.

## Determinism and reconstruction

Several equally short paths may exist. This teaching contract breaks ties first by smaller remaining distance, then insertion order. Right/down/left/up neighbor insertion makes that order reproducible. Store the predecessor that produced a strictly better cost; do not replace it for equal cost. Backtracking from the goal then reconstructs one specified shortest route.

In an empty 3×3 grid from $(0,0)$ to $(2,2)$, the path follows right, right, down, down under these ties. It has four moves. With 0.5 m cells, metric cost is 2 m. A blocked center changes available routes but not necessarily the optimal cost.

## Visual explanation

Display open/closed search states, obstacles, start/goal, and the reconstructed route. Selecting a cell reveals its best cost, heuristic, priority, and predecessor. A step table provides the same trace without relying on color or animation.

## Robot relevance and failure modes

A point-robot path can collide when executed by a wide robot; footprint inflation must happen before this lesson's planner. Row/column swaps can produce a plausible route through the wrong map. A diagonal shortcut violates the motion model even if it is shorter on screen. This foundation makes later learned-planning papers easier to assess: route validity, cost, and collision checks remain necessary regardless of how candidates are generated.

