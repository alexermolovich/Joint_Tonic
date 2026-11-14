# Progressive hints

## Hint 1

Use the mean wheel travel for midpoint arc length and the right-minus-left difference for heading change.

## Hint 2

A turning robot follows an arc. Integrate that arc in the world frame rather than translating the full distance along the old heading.

## Hint 3

Check the straight-motion limit and pure rotation separately. If using sinc, verify whether the chosen definition includes pi, and normalize heading only after computing displacement.
