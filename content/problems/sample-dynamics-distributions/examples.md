# Worked sampling outputs and boundaries

The full bounds and draws are in statement.md.

1. Lower endpoint row yields mass 1 kg, friction 0.25, delay 0 ticks, gain scale 0.5, delay 0 seconds. Midpoint row yields mass 3 kg, friction 0.5, delay 2 ticks, gain scale 1, delay 0.02 seconds.
2. Fixed ranges yield mass 2 kg, friction 0.5, delay 1 tick, gain scale 1, delay 0.02 seconds for every valid row.

For delay bounds (0,3), the unit-draw buckets are:

| Unit draw interval | Output ticks |
|---|---:|
| [0,0.25) | 0 |
| [0.25,0.5) | 1 |
| [0.5,0.75) | 2 |
| [0.75,1) | 3 |

A draw equal to 1 raises ValueError rather than producing tick 4. An empty float64 array of shape (0,4) produces all five empty arrays with their specified dtypes.

Theory answers: a log midpoint gives a geometric mean; a control tick may span multiple physics substeps, so the same integer count can imply different delays. These are synthetic teaching configurations, not hardware-safe recommendations.
