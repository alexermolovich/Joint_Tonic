# Progressive hints

## Hint 1

The last column of `T` describes the camera origin in world coordinates. The upper-left `3×3` block describes the camera basis expressed in world coordinates. Keep those two roles separate.

## Hint 2

The equation uses a column point, but the batch stores row points. Work out the transpose needed for `(N,3) @ (3,3)`. A `(3,)` translation can broadcast across every row.

## Hint 3

Validate the transform before handling the batch: bottom row, orthogonality, and determinant are independent checks. Preserve `(0,3)` for an empty batch. Even identity should return newly computed storage rather than the original input.
