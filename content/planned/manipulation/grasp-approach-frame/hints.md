# Progressive hints

## Hint 1

Identify which column of a world-from-grasp rotation describes the grasp z-axis in world coordinates.

## Hint 2

The pre-grasp must reach the target after moving along positive tool z, so its offset points in the opposite direction.

## Hint 3

Keep rotation unchanged and apply the offset only to translation. Check a rotated tool to catch code that always subtracts from world z.

