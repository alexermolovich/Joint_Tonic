# Rewire a Tree Without Creating Cycles

## Intuition

A cheaper parent can improve an entire subtree. The tree structure must remain valid, and every descendant inherits the changed root-path cost even though its own edge stays the same.

## Mathematics and conventions

Let parent index $p_i$ and edge cost $e_i\ge0$ define root cost $C_0=0$ and $C_i=C_{p_i}+e_i$. A proposal attaches vertex v to parent u with cost c. Accept only when the supplied edge is feasible, u is outside v's subtree, and

$$C_u+c<C_v.$$

For each descendant j of v, the path cost changes by the same amount

$$\Delta=C_u+c-C_v,\qquad C'_j=C_j+\Delta.$$

Costs have one common normalized path-cost unit; node IDs are identifiers, not coordinates. Computing costs by a root-first traversal also detects components that cannot reach the root. This implements one deterministic rewire, not the RRT* sampling loop.

## Visual computation trace

| Node | Original parent/cost | After attaching 1 to 3 |
| --- | --- | --- |
| 0 | root / 0 | root / 0 |
| 1 | 0 / 5 | 3 / 2 |
| 2 | 1 / 7 | 1 / 4 |
| 3 | 0 / 1 | 0 / 1 |

## Worked examples

1. Parents `[-1,0,1,0]`, edge costs `[0.,5.,2.,1.]`, vertex `1`, new parent `3`, connection cost `1`, feasible True yield parents `[-1,3,1,0]`, edge costs `[0.,1.,2.,1.]`, root costs `[0.,2.,4.,1.]`, changed True.
2. With the same original tree, connecting vertex `1` beneath vertex `2` would form a cycle. Return unchanged parents and edges, root costs `[0.,5.,7.,1.]`, changed False.

## Why this matters on a robot

Updating only the rewired vertex leaves stale descendant costs and can corrupt later parent selection. A supplied feasible flag is only as good as its collision checker; this task does not turn sampled checks into a continuous safety guarantee.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1005.0416). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
