# Worked inputs and expected outcomes

## Example 1: a right-angle elbow

`L1=1, L2=1, target=[1,1]`.

Expected: `reachable=True, angles=[0,pi/2], singular=False`. The first link ends at `[1,0]`; the second turns upward and reaches `[1,1]`.

The alternative elbow branch is intentionally not returned.

## Example 2: extension and an unreachable neighbor

`L1=2, L2=1, target=[3,0]`.

Expected: `reachable=True, angles=[0,0], singular=True`. The links align along base +x.

For the same arm and target `[4,0]`, expected: `reachable=False, angles=None, singular=False`. Its radius 4 exceeds the maximum reach 3 by much more than tolerance.
