# Reject Inconsistent Loop Closures

## Intuition

A plausible place match can still imply an inconsistent pose jump. Normalize the supplied pose discrepancy by its uncertainty, then combine it with overlap and separation checks while retaining one deterministic reason for rejection.

## Mathematics and conventions

For candidate $k$, residual $r_k\in\mathbb R^6$ orders translation meters then rotation radians. Its symmetric positive covariance $C_k\in\mathbb R^{6\times6}$ has entry units equal to the product of those coordinate units, including meter-radian cross terms. Compute
$$d_k^2=r_k^\top C_k^{-1}r_k.$$
Solve a linear system rather than explicitly inverting $C_k$. Its minimum eigenvalue must be at least $\max(10^{-9},10^{-8}\lambda_{\max})$ under the specified numerical coordinate scaling. For supplied overlap $o_k\in[0,1]$, elapsed time $t_k$ seconds, and gates $\tau,o_{\min},t_{\min}$,
$$a_k=(d_k^2\le\tau)\land(o_k\ge o_{\min})\land(t_k\ge t_{\min}).$$
Reasons prioritize short elapsed time, then insufficient overlap, then excessive normalized discrepancy. This is an original operational gate for supplied evidence; it is not the paper's ICP fitness rule or a calibrated probability of correctness.

## Visual computation trace

| Check in order | Failure code | Required evidence |
|---|---|---|
| Elapsed seconds | 1 | elapsed ≥ minimum |
| Overlap fraction | 2 | overlap ≥ minimum |
| Covariance-normalized discrepancy | 3 | squared distance ≤ threshold |
| All pass | 0 | Accept supplied candidate |

## Worked examples

1. Residual [2,0,0,0,0,0], identity covariance, overlap 0.5, elapsed 10 seconds, and gates (4,0.5,10) give squared distance 4, accepted True, reason 0. Boundaries are inclusive.
2. A candidate with elapsed 9, overlap 0 and large residual receives reason 1 when minimum elapsed is 10: the temporal reason takes precedence over the other failures.

## Why this matters on a robot

A wrong loop can bend an entire map. Ignoring covariance cross terms changes the discrepancy score, while treating a covariance gate as a probability guarantee ignores how that covariance was estimated. Accepted evidence still needs trustworthy registration and calibration.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2007.00258). [mahalanobis-measurement-gate](/problems/mahalanobis-measurement-gate)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
