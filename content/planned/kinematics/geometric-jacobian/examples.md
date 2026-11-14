# Worked inputs and expected outcomes

## Example 1: a two-meter lever arm

One revolute joint: origin `[0,0,0]`, axis `[0,0,1]`; tool `[2,0,0]`.

Expected Jacobian column: `[0,2,0,0,0,1]`. A joint rate of `0.5 rad/s` gives twist `[0,1,0,0,0,0.5]`.

## Example 2: add a prismatic axis

Use the same revolute joint plus a prismatic joint with base-frame axis `[1,0,0]`. The second joint's origin is irrelevant to its translational column.

Expected Jacobian:

`[[0,1],[2,0],[0,0],[0,0],[0,0],[1,0]]`.

For rates `[0.5,0.2]`, expected twist: `[0.2,1,0,0,0,0.5]`. The second rate is meters per second, not radians per second.
