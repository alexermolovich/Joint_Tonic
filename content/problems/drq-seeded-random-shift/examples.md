## Example 1

An image array of shape (1, 2, 1, 1, 1), with frame values 0.2 and 0.8, remains unchanged after any padding-1 edge crop. Both frames share the same generated offset.

## Example 2

Padding 0 returns a fresh copy of the entire input and offsets [[0, 0]] for a one-row batch, for any valid seed.
