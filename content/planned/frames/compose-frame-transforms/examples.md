# Worked inputs and expected outcomes

These examples are hand-checkable planning fixtures; no evaluator exists yet.

## Example 1: a mounting offset rotates with the base

`T_wb` has rotation `[[0,-1,0],[1,0,0],[0,0,1]]` and translation `[1,0,0]`. `T_bc` has identity rotation and translation `[1,0,0]`.

Expected: `T_wc` has the same 90-degree rotation and translation `[1,1,0]`. Its inverse has rotation `[[0,1,0],[-1,0,0],[0,0,1]]` and translation `[-1,1,0]`.

The camera origin travels from camera `[0,0,0]` to base `[1,0,0]` to world `[1,1,0]`.

## Example 2: two translations

`T_wb` translates by `[2,0,0]`; `T_bc` translates by `[0,3,0]`. Both rotations are identity.

Expected camera-to-world translation: `[2,3,0]`. Expected world-to-camera translation: `[-2,-3,0]`. Camera point `[1,1,0]` becomes world point `[3,4,0]` and returns unchanged after inversion.
