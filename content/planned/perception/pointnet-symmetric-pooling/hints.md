# Hints

## Hint 1

The point axis is axis 1, so the two remaining axes should be B and D.

## Hint 2

A mask of shape (B,N) needs a feature dimension when combined with (B,N,D). Invalid slots must be unable to win a maximum.

## Hint 3

To test invariance, use the same per-cloud permutation on feature rows and their validity mask. Also test all-negative valid features.
