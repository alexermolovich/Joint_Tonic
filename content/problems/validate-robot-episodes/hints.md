# Progressive hints

## Hint 1

Separate errors in the caller's schema from anomalies in episode data. Invalid schema settings raise `ValueError`; supported episode anomalies become issue records with an episode index, path, and code.

## Hint 2

Follow the documented validation hierarchy. Check the container and row count first, then row shape, dtype, finiteness, and range. Avoid several downstream complaints caused by the same malformed row.

## Hint 3

Missing rows use a signal-level fraction check; metadata has its own paths. Append each supported issue without mutating data, then sort once by `(episode,path,code)` to make the report stable across dictionary traversal order.
