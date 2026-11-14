# Extract Mutual Matches and Unmatched Labels from Transport Scores

Implement `mutual_matches(assignment, threshold)`.

Extract confident reciprocal feature assignments with deterministic ties and explicit unmatched labels.

`assignment` is float64 `(N+1,M+1)`, `0<=N,M<=1024`, `N*M<=262144`, finite values in `[0,1e6]`. The final row and column are dustbins. The input is supplied transport evidence; no marginal normalization is required here. `threshold` is a Python int/float in `[0,1e6]`.

For each real source row, choose the largest value among real target columns, breaking exact ties by the first column. For each real target column choose the first largest real source row. Retain a pair only if those choices are reciprocal and its score is strictly greater than threshold. Ignore dustbins in both argmax operations. Optional dustbin-dominance rejection belongs to the separate prerequisite and is not automatically applied by this function.

Return `matches_source`, int64 `(N,)`, and `matches_target`, int64 `(M,)`, with -1 for unmatched points; `confidence_source`, float64 `(N,)`, and `confidence_target`, float64 `(M,)`, zero for unmatched points; and `pairs`, int64 `(K,2)` ordered by ascending source index. Empty sides yield all unmatched labels and a `(0,2)` pairs array. All arrays are fresh. This is confidence/mutual extraction only, not a training loss or geometric verification.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Assignment `[[0.8,0.1,0.],[0.2,0.7,0.],[0.,0.,0.]]`, threshold 0.5: pairs `[[0,0],[1,1]]`, source and target matches `[0,1]`, confidence `[0.8,0.7]`.
2. An all-ones real `2x2` block with threshold 0 has only pair `[[0,0]]`: first-index argmax ties must be reciprocal. With threshold 1 no pair passes the strict comparison.

## Source and scope

[Primary source](https://arxiv.org/abs/1911.11763). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
