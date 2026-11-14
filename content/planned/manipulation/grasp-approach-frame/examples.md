# Hand-verified worked examples

**Planning examples, not executable tests.** Values below define the intended contract and must be reproduced by the future reference implementation.

## Example 1: world-aligned tool

Input rotation=identity; target translation=(0.4,0.2,0.3) m; distance=0.1 m.

Expected pre-grasp translation=(0.4,0.2,0.2) m. Rotation remains identity.

The positive local z approach travels upward by 0.1 m to the target.

## Example 2: sideways approach

Input rotation rows=[[0,0,1],[0,1,0],[-1,0,0]]; target translation=(1,0,0.5) m; distance=0.2 m.

The third rotation column is (1,0,0), so the tool approaches along world x.

Expected pre-grasp translation=(0.8,0,0.5) m; rotation unchanged.

## Boundary

Distance=0 preserves the target pose values but must still return independent storage and validate the transform.

