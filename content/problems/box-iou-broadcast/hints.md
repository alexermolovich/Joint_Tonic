# Progressive hints

## Hint 1

The intersection starts at the larger lower corner and ends at the smaller upper corner. Clamp each resulting width and height to zero before multiplying them.

## Hint 2

Insert distinct singleton axes: A becomes `(N,1,4)` and B becomes `(1,M,4)`. Broadcasting then computes every pair without assuming that N equals M.

## Hint 3

Build areas with shapes `(N,1)` and `(1,M)` before forming union. Divide only where union is positive, using zero elsewhere. This also gives the documented behavior for zero-area boxes and correctly shaped empty sets.
