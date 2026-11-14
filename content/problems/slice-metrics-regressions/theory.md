# Compare Slice Metrics Without Hiding Regressions

## Intuition

A new policy may improve the common easy scenarios while getting worse on rare high-delay episodes. Keep the pooled change and every declared scenario slice visible so the overall average cannot erase that regression.

## Paired changes, explicit coverage

For paired episode $i$, let $b_i$ and $c_i$ be dimensionless baseline and candidate losses. Define $d_i=c_i-b_i$. For slice $s$ with index set $I_s$,

$$\Delta_s=\frac1{|I_s|}\sum_{i\in I_s}d_i,\qquad R_s=\mathbf1[\Delta_s>\tau].$$

$\tau$ is the supplied nonnegative loss tolerance. An empty $I_s$ has unknown delta and a false flag, accompanied by `complete=False`. The pooled change is

$$\Delta_{all}=\frac1N\sum_i d_i,$$

which weights slices by their observed episode counts. It is not the equally weighted mean of slice deltas.

## Visual regression trace

| Slice | Paired deltas | Slice mean | Regression at tolerance 0 |
|---|---|---|---|
| nominal | [-2,-2] | -2 | no |
| high_delay | [3] | 3 | yes |

Overall $\Delta_{all}=-1/3$ improves, but the high-delay slice regresses. This table is the static visual and text alternative.

## Why this matters on a robot

Comparing unpaired episode sets can mistake scenario mix changes for model improvements. Missing rare slices are unknown evidence. This diagnostic reports observed changes, not statistical significance or causal attribution.

Prerequisite: [Measure Performance Across Shift Buckets](/problems/shift-bucket-performance).

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
