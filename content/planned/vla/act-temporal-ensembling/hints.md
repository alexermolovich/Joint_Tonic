# Progressive hints

## Hint 1

Compute each candidate offset from the target tick and its own start. Filter by both horizon bounds and valid before assigning ranks.

## Hint 2

Use ranks0,1,... only for surviving rows. With decay0, every eligible row has equal weight regardless of start-tick gaps.

## Hint 3

Place normalized weights back into a length-C zero array. Multiply only aligned predictions, accumulate in float64, and cast the final arrays to the original float dtype.
