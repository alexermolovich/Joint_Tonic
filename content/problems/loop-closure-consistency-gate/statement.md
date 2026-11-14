# Reject Inconsistent Loop Closures

Implement `gate_loop_closures(residuals, covariance, overlap, elapsed, threshold, min_overlap, min_elapsed)`.

`gate_loop_closures(residuals, covariance, overlap, elapsed, threshold, min_overlap, min_elapsed)` residuals(K,6),0<=K<=8192, translation meters + rotation radians supplied same tangent convention; covariance(K,6,6),symmetric atol1e-9  then average,positive eigenvalues satisfy lambda_min>=max(1e-9,lambda_max*1e-8). overlap(K)fraction[0,1],elapsed(K)seconds[0,1e6];thresholdscalar [0,1e6]on squared Mahalanobis,min_overlap[0,1],min_elapsed[0,1e6].

Return squared_distance(K)=r.Tsolve(C,r),accepted(K)=(d<=threshold)&(overlap>=min)&(elapsed>=min),reason int64(K) priority1 elapsed too short,2 overlap low,3 Mahalanobis too large,0 accepted.

All values validated even rejected for earlier reasons.

Covariance cross terms matter.

Original operational consistency gate for supplied registration evidence; not LIO-SAM's actual ICP fitness heuristic, a probability guarantee, or loop proposal/registration.

Example: r=[2,0,0,0,0,0],C=I,threshold4,overlap.5,min.5,elapsed10,min10=>d4accepted.

Example: elapsed9 andoverlap0 andlarge error=>reason 1; empty arrayscorrectshapes.

Covariance entry C[i,j] has the product of residual coordinate i and j units (m², m·rad, or rad²).

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Residual [2,0,0,0,0,0], identity covariance, overlap 0.5, elapsed 10 seconds, and gates (4,0.5,10) give squared distance 4, accepted True, reason 0.

Boundaries are inclusive.
2. A candidate with elapsed 9, overlap 0 and large residual receives reason 1 when minimum elapsed is 10: the temporal reason takes precedence over the other failures.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.00258).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
