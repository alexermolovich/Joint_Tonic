## Example 1

Logged values [[1, 3]] and sampled values [[5]], all valid, have means 2 and 5. The gap is 3, counts are [[2, 1]], and threshold 2 produces flagged = [True].

## Example 2

With the same values and threshold 3, equality is not flagged. If the sampled mask is all false, its mean and the gap are NaN, and flagged is false.
