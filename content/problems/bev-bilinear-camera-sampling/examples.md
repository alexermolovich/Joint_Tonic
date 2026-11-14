## Worked examples

**Example 1.** One camera has a single-channel map `[[0, 2],[4, 6]]`. A valid point `(u=.5, v=.5)` samples value `3`, with `used=True`.

**Example 2.** For the same map, points `(1, 1)` and `(1.1, 1)` produce samples `6` and `0`. The returned used mask is `[True, False]`; the second point is outside.
