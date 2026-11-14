# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Normalize rows, compute pairwise Euclidean distances, mask the diagonal to infinity, choose the smallest-index minimum, then clamp only the logarithm argument.
3. Use the worked trace to check axis order and boundary conventions.
