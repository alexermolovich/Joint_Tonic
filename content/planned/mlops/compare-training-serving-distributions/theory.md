# Compare Training and Serving Distributions

## Intuition

A robot's serving logs may contain more night scenes than its training set. Comparing raw counts confuses changing workload with changing composition. Normalize each histogram separately, then compare categories with the same meanings.

## Align before subtracting

Let C be the union of category names. Training count $a_c$ and serving count $b_c$ are nonnegative integers; absent categories have count zero. Totals A and B must be positive. Define

$$
p_c=\frac{a_c}{A},\qquad q_c=\frac{b_c}{B},
\qquad \Delta_c=q_c-p_c,\qquad
d_\infty=\max_{c\in C}|\Delta_c|.
$$

Probabilities, differences and distance are dimensionless. The sign of $\Delta_c$ distinguishes increased from decreased representation. A supplied threshold $\theta\in[0,1]$ flags the histogram exactly when $d_\infty>\theta$.

The metric does not account for finite-sample uncertainty. Ten observations and ten million can produce the same distance with different confidence. Do not claim that this threshold comparison is a hypothesis test.

## Visual: aligned operating conditions

| Category | Train probability | Serve probability | Serve minus train |
|---|---:|---:|---:|
| dry | 0.75 | 0.5 | -0.25 |
| snow | 0 | 0.5 | 0.5 |
| wet | 0.25 | 0 | -0.25 |

Read across each row, then take the largest absolute difference:0.5. The table is also the text alternative. Dropping unknown categories would miss the largest change in this example.

## Why this matters on a robot

A small overall shift can still be important if it affects a rare condition such as a slippery floor. Category naming and scenario slices must stay consistent across training and serving. Different label taxonomies or changed logging rates can create apparent shifts unrelated to physical changes. Version the histogram definitions alongside the data.

## Check your understanding

1. Why normalize training and serving by different totals?
2. Why reject an empty histogram rather than assume a uniform distribution?

## Sources and prerequisites

The paper motivates comparisons of dataset statistics. This aligned maximum-frequency-difference contract is an explicit teaching metric; its threshold is supplied and is not a statistical significance test or complete drift detector. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/), Section4: detecting training/serving skew with dataset statistics. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.
