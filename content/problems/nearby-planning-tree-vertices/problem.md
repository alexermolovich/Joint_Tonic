# Find Nearby Planning Tree Vertices

Implement `nearby_vertices(vertices, query, weights, radius)`.

Find tree vertices inside an inclusive weighted configuration-space radius.

`vertices` float64 `(N,D)`, `0<=N<=100000`, `1<=D<=16`; `query` float64 `(D,)`; `weights` float64 `(D,)` with values >=1e-9. All coordinates and weights are dimensionless normalized configuration features, already scaled consistently upstream. `radius` is Python int/float in `[0,1e6]` in the resulting dimensionless metric. Squared distance is sum(weights*(vertex-query)²). Return `(indices, distances)`: fresh int64 `(K,)` original indices with squared distance <=radius², in ascending index order, and float64 `(K,)` square-root distances for those indices. Do not sort by distance. Empty vertices return empty outputs. There is no angular wrapping, collision check, timestamp dependence, or RRT* radius schedule in this component.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Vertices `[[0.,0.],[1.,0.],[0.,2.]]`, query `[0.,0.]`, weights `[4.,1.]`, radius2 gives indices `[0,1,2]` and distances `[0.,2.,2.]`; boundary vertices are included.
2. Vertices `[[1.],[0.],[0.]]`, query `[0.]`, weight `[1.]`, radius0 gives indices `[1,2]`, distances `[0.,0.]`, preserving duplicates and index order.

## Source and scope

[Primary source](https://arxiv.org/abs/1005.0416). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
