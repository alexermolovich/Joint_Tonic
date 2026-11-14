# Build a Feature-Matching Score Matrix

Implement `feature_scores(source_descriptors, target_descriptors)`.

Compute pairwise scores from two supplied sets of learned image descriptors.

`source_descriptors` is float64 `(N,D)` and `target_descriptors` float64 `(M,D)`, `0<=N,M<=1024`, `N*M<=262144`, `1<=D<=128`, all values with absolute magnitude <=100. Descriptor channels are dimensionless. Return a fresh float64 `(N,M)` matrix with `S[i,j]=dot(source_descriptors[i],target_descriptors[j])/sqrt(D)`.

Descriptors need not have unit norm. Do not normalize descriptor rows, apply softmax, or add dustbins. Empty point sets return the exact corresponding empty matrix shape. This isolates an explicit supplied-feature similarity convention; the descriptors are already produced by a separate learned network. It does not implement contextual graph refinement or training.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With D=1, source `[[2.],[3.]]` and target `[[4.]]` give scores `[[8.],[12.]]`.
2. With D=4 and both sets containing one descriptor `[1.,1.,1.,1.]`, the dot product 4 is divided by sqrt(4), giving `[[2.]]`. Cosine similarity would incorrectly give 1.

## Source and scope

[Primary source](https://arxiv.org/abs/1911.11763). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
