# Benchmark Detector Accuracy Against Edge Latency

## Intuition

There is rarely one detector that wins every metric. Remove candidates that are worse in both accuracy and latency, then choose the best remaining option that meets the operating deadline.

## Math and decision table

Candidate $i$ has dimensionless accuracy $a_i$ and latency $\ell_i$ milliseconds. Candidate $j$ dominates it when
$$a_j\ge a_i,\quad \ell_j\le\ell_i,\quad (a_j>a_i\;\lor\;\ell_j<\ell_i).$$
The frontier $F$ contains candidates with no dominator. With budget $B$ milliseconds, select the feasible index minimizing the lexicographic tuple $(-a_i,\ell_i,i)$ among $\ell_i\le B$.

| Candidate | Accuracy | Latency ms | Decision at B=20 ms |
|---|---|---|---|
| 0 | 0.70 | 10 | fast frontier option |
| 1 | 0.80 | 20 | best feasible |
| 2 | 0.75 | 25 | dominated by 1 |

Equality at the budget is allowed. Equal accuracy favors lower latency, then earlier input index. Exact duplicates remain on the frontier because domination requires at least one strict improvement.

## Why this matters on a robot

A higher detector score is not helpful if inference misses the sensing deadline. Comparisons require matching hardware, precision, preprocessing and latency percentile; heterogeneous measurements form a misleading frontier. This exercise analyzes supplied measurements and does not certify real-time safety.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1506.02640). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
