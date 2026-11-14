# Interpolate Joint State at Camera Time

**Status: planned.** A camera frame arrives between two joint-state measurements. Estimate the joint positions at its measurement timestamp while recognizing gaps with insufficient evidence.

## Contract

Inputs are finite strictly increasing source timestamps `times (T,)`, `T>=2`, finite joint positions `q (T,D)`, `D>=1`, finite camera query times `queries (M,)`, and finite positive `max_gap`. All times share one clock in seconds. Joint angles are radians and already unwrapped; interpolate each channel linearly.

Return new float64 `aligned (M,D)` and bool `valid (M,)`. An exact source timestamp returns its recorded state and is valid. Otherwise interpolate only when the query is bracketed by source timestamps whose gap is at most `max_gap`. Unbracketed queries or excessive gaps return NaN rows and false validity.

Do not extrapolate, substitute the nearest sample, estimate clock offset, or wrap angles. Query order is preserved and need not be sorted. Empty queries are valid. Reject duplicate/decreasing times, nonfinite values, bad shapes, or invalid gap limits.

See [examples](examples.md), [theory](theory.md), and [hints](hints.md).
