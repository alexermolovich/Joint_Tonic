# Worked inputs and expected outcomes

## Example 1: straight travel from a rotated heading

Initial pose `[1,2,pi/2]`; left and right travel `0.5 m`; track width `0.4 m`.

Expected pose: `[1,2.5,pi/2]`, within numerical tolerance. Equal travel causes no heading change; robot forward aligns with world +y.

## Example 2: a quarter-circle turn

Initial pose `[0,0,0]`; left travel `0`; right travel `pi/2 m`; track width `1 m`.

Expected pose: `[0.5,0.5,pi/2]`. Mean travel is `pi/4`, heading change is `pi/2`, and arc radius is `0.5 m`.

For a separate in-place turn with left `-pi/4` and right `pi/4`, expected pose is `[0,0,pi/2]`: zero mean travel gives no midpoint translation.
