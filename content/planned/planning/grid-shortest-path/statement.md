# Plan a Shortest Route on an Occupancy Grid

**Status: planned; no runnable implementation yet.**

A mobile robot has a binary map and must reach a goal cell. Plan a shortest four-neighbor route while making coordinate and tie conventions explicit.

## Contract

Planned function: grid_plan(occupied, start, goal, cell_size).

The nonempty rectangular boolean grid uses row increasing downward and column increasing rightward. True means blocked. Start and goal are integer (row,column) pairs within the grid. Cell size is finite and positive meters. Movement uses right, down, left, up neighbors; diagonals are forbidden.

Use A* with Manhattan remaining-step distance. Priority is (total estimated steps, remaining steps, insertion order); insert neighbors in the declared order. Ignore stale queue entries and never replace an equal-cost predecessor. Return status, path including both endpoints, and metric cost. An unreachable or blocked endpoint returns status=unreachable, empty path, and cost_m=None. A free start equal to goal succeeds at zero cost. Invalid shape, coordinates, or cell size raise an error.

## Assessment plan

Check every path edge, obstacle avoidance, optimal length, stable tie behavior, and disconnected maps. The map is already inflated for robot footprint. See [examples.md](examples.md). This folder is planned; no executable planner is provided.

