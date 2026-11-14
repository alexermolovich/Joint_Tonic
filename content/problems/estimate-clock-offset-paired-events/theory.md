# Estimate Clock Offset from Paired Events

## Intuition

Before synchronizing sensors, separate their clock origins. A median offset resists a few delayed or mismatched events better than a mean, while residuals reveal disagreement that one offset cannot explain.

## Mathematics and physical meaning

Let $a_i,b_i$ denote timestamps of the same event in two clocks, in seconds. Differences $d_i=b_i-a_i$ estimate the clock offset. Compute
$$\widehat\delta=\operatorname{median}_i d_i,\qquad e_i=d_i-\widehat\delta.$$
The output residual $e_i$ is in seconds. Correct clock B using $b_i-\widehat\delta$. This model assumes unit clock-rate ratio; steadily changing residuals suggest drift, which a constant cannot remove.

## Visual trace

| Event | Difference B-A (s) | Offset (s) | Residual (s) |
|---|---|---|---|
| 0 | 2 | 2 | 0 |
| 1 | 2 | 2 | 0 |
| 2 | 9 | 2 | 7 |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `clock_a=[0,1,2], clock_b=[2,3,11]` → `(2.0,[0,0,7])`. One delayed event does not move the median.
2. `clock_a=[1,2], clock_b=[0,3]` → `(0.0,[-1,1])`. The two middle differences average to zero.

## Why this matters on a robot

A wrong sign doubles synchronization error. This result is an offset estimate, not a guarantee of causal pairing; biased transport delays or half the pairs being wrong can defeat the median. Track residuals as calibration health evidence.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
