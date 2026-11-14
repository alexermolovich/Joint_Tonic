# Hints

## Hint 1

Write down the output location of one pixel that lies in the second grid column. That exposes an incorrect plain reshape.

## Hint 2

Separate both spatial dimensions into a grid dimension and a local-patch dimension before reordering.

## Hint 3

Derive the inverse permutation; then test both exact token values and the round trip. Copy the final result so even P=1 does not alias the input.
