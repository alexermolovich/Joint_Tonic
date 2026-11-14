# Hand-verified worked examples

**Planning examples, not executable tests.** Values below define the intended contract and must be reproduced by the future reference implementation.

## Example 1: between two waypoints

Inputs: times=[0,2,5] s; positions=[[0,0],[2,-2],[5,1]] rad; query=1 s.

The first interval has fraction 0.5.

Expected position=[1,-1] rad; velocity=[1,-1] rad/s.

## Example 2: query at an interior knot

Use the same trajectory and query=2 s.

Expected position=[2,-2] rad; velocity=[1,1] rad/s.

The right interval runs from 2 to 5 seconds, with displacement [3,3] over 3 seconds.

## Boundary

Query=6 s returns position=[5,1] and velocity=[0,0]. Endpoint holding is deliberate; extrapolating the last slope would violate this contract.

