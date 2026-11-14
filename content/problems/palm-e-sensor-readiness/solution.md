## Approach

Broadcast current time and per-sensor age limits, compute stale/usable separately, then reduce the required-sensor implication across modalities.

O(B*M) time and space.
