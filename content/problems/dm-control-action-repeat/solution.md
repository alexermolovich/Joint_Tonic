# Solution explanation

Validate complete arrays before examining the consumed prefix. Accumulate float64 reward and discount in chronological order; include the LAST transition, then break. The scan is O(T) including validation and uses constant extra state.
