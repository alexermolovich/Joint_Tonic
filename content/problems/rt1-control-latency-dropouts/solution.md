## Approach

Validate synchronized rows, subtract delivered timestamps, fill missing latencies with -1, then reduce the explicitly different masks and denominators.

O(T) time and O(T) output storage.
