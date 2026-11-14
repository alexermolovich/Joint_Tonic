# Associate Scan Points with Local Map Planes

Implement `associate_planes(queries, map_points, neighbors, max_neighbor_distance, plane_tolerance)`.

Associate each deskewed world-frame scan query with a deterministic local plane fitted to nearby map points.

`queries` is float64 `(N,3)`, `0<=N<=256`; `map_points` is float64 `(M,3)`, `3<=M<=4096`; require `N*M<=1_000_000`. Points share a right-handed world frame and meter units. `neighbors` is a Python int in `[3,min(16,M)]`; `max_neighbor_distance` a Python int/float in `[1e-6,1e6]` meters; `plane_tolerance` a Python int/float in `[0,100]` meters.

Choose exactly K nearest map points by `(squared_distance, original_map_index)`. Compute their centroid and population covariance. Let eigenvalues be ascending lambda0,lambda1,lambda2. A fit is valid iff every selected point is within the radius of the query (equality allowed), lambda1>1e-8 square meters, lambda1-lambda0>1e-8 square meters, and every neighbor's absolute distance to the fitted plane is <=plane_tolerance. The second eigenvalue rejects collinear support; the eigenvalue gap rejects an ambiguous least-variance axis.

Use the unit eigenvector of lambda0 as normal, orienting it so its largest-absolute component is positive; exact component ties choose the first axis. Return `neighbor_indices` int64 `(N,K)` and `centroids` float64 `(N,3)` for every query, `normals` float64 `(N,3)` and `offsets` float64 `(N,)` where plane equation is normal dot point + offset=0, and `valid` bool `(N,)`, in a dictionary. Invalid normals/offsets are NaN; their neighbors/centroids remain available. Empty queries are valid. This original brute-force association and plane-fit policy illustrates the local-map mechanism; it does not reproduce FAST-LIO2's ikd-Tree or iterated filter.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Map corners `[[-1.,-1.,0.],[-1.,1.,0.],[1.,-1.,0.],[1.,1.,0.]]`, query `[[0.,0.,1.]]`, K=4, radius 2, tolerance 0 yield centroid `[[0.,0.,0.]]`, normal `[[0.,0.,1.]]`, offset `[0.]`, valid `[True]`. Equal-distance neighbor indices follow `[0,1,2,3]`.
2. Map points on one straight line, such as `[[0.,0.,0.],[1.,0.,0.],[2.,0.,0.]]`, have zero second eigenvalue. The fit is invalid and normal/offset are NaN, even if every neighbor is within radius.

## Source and scope

[Primary source](https://arxiv.org/abs/2107.06829). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
