# Progressive hints

## Hint 1

Map each dimension independently. A translation channel's bounds may be in meters while a rotation channel's bounds are in radians; broadcasting the `(D,)` bounds preserves that distinction.

## Hint 2

Clip physical values before normalizing. Flooring the normalized position times the number of bins gives the bin ID, except that the exact upper bound must be clamped to the last valid ID.

## Hint 3

Apply the vocabulary offset only to tokens. Decode the unshifted bin ID at its center in physical units. Check that increasing the offset changes the integer IDs without changing the reconstructed actions.
