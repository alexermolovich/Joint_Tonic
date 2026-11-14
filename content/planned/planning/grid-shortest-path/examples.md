# Hand-verified worked examples

**Planning examples, not executable tests.** Values below define the intended contract and must be reproduced by the future reference implementation.

## Example 1: an open grid

Grid: three rows of [False,False,False]. Start=(0,0), goal=(2,2), cell_size=0.5 m.

Expected path: [(0,0),(0,1),(0,2),(1,2),(2,2)].

Expected status=success; cost_m=2.0.

There are four cell transitions. The declared tie policy selects the top-row-first route.

## Example 2: a wall forces a detour

Grid:
- [False,True,False]
- [False,True,False]
- [False,False,False]

Start=(0,0), goal=(0,2), cell_size=1 m.

Expected path: [(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2)].

Expected status=success; cost_m=6.0.

## Boundary

If the wall fills the third row's middle cell too, the two sides are disconnected. Return unreachable, an empty path, and no metric cost.

