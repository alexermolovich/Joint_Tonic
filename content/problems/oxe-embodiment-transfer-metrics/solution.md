## Approach

Accumulate a count/success matrix, divide nonempty cells only, then separately reduce diagonal and off-diagonal episode outcomes.

O(N+E^2) time and O(E^2) storage.
