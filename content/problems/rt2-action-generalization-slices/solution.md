## Approach

Count slice membership, accumulate invalid and valid-success counts, and divide with an explicit nonempty mask. Preserve every declared slice.

O(N+S) time and O(S) output.
