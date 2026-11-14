# Hints

## Hint 1

Start with a Q-by-M view of class probabilities by indexing the target labels. Do not include the final background column as a target.

## Hint 2

Broadcast boxes as (Q,1,4) and (1,M,4). Keep the L1 computation in center/size format; convert a separate copy for area calculations.

## Hint 3

For disjoint boxes, clamp intersection side lengths at zero, but do not clamp GIoU to zero. Verify the signs with an identical-box pair.
