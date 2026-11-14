# Hand-verified worked examples

**Planning examples, not executable tests.** Values below define the intended contract and must be reproduced by the future reference implementation.

## Example 1: clear endpoints, blocked interior

Inputs: start=(0,0), end=(4,0), obstacles=[[2,-1,3,1]], clearance=0.

Expected: free=False; first_obstacle=0; entry_t=0.5.

At t=0.5, the center reaches (2,0), the obstacle's left boundary.

## Example 2: a clearance margin changes the answer

Inputs: start=(0,2), end=(4,2), obstacles=[[2,-1,3,1]], clearance=0.

Expected: free=True; first_obstacle=None; entry_t=None.

With clearance=1, expanded bounds become [1,-2,4,2].

Expected: free=False; first_obstacle=0; entry_t=0.25.

The center first touches the expanded top boundary at (1,2).

## Boundary

A zero-length segment at (2.5,0) inside the original box collides at entry_t=0.

