# Progressive hints

## Hint 1

Construct each requested index as start_indices[:,None]+arange(horizon)[None,:]. Derive validity before gathering.

## Hint 2

Out-of-range indices must not reach array indexing. Use safe temporary indices or copy only valid entries, then set invalid entries to zero.

## Hint 3

Preserve start order and duplicates. Allocate independent outputs so a view of actions cannot leak mutations into the recorded dataset.
