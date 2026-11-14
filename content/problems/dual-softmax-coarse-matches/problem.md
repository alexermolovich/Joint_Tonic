# Construct Coarse Correspondence Candidates

Implement `coarse_matches(source, target, source_valid, target_valid, temperature, threshold)`.

Construct coarse correspondences with masked dual-softmax confidence and reciprocal choices.

`source (N,D)` and `target (M,D)` are float64, `0<=N,M<=512`, `1<=D<=128`, absolute entries <=100. `source_valid (N,)` and `target_valid (M,)` are bool. `temperature` is a Python int/float in `[1e-3,100]`; `threshold` in `[0,1]`.

Compute dimensionless similarities `S=source@target.T/(D*temperature)`. The factor D corresponds to dividing each descriptor by sqrt(D) before forming its dot product. A pair is valid iff both endpoints are valid. Compute row softmax over valid target columns and column softmax over valid source rows, multiply the two probabilities, and set invalid pairs to zero. If an axis has no valid support, its confidence values are zero.

Choose each valid source's first maximal real target confidence and each valid target's first maximal real source confidence. Retain reciprocal pairs with confidence strictly greater than threshold. Return fresh float64 `confidence (N,M)`, int64 `pairs (K,2)` in ascending source order, and float64 `match_confidence (K,)`. Empty or fully masked sides return zero confidence and no pairs. First-index ties are a deterministic teaching convention. Border-removal heuristics, training padding, positional encoding and full network inference are outside this component.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Two zero source descriptors and two zero target descriptors, D=1, all valid, temperature 1: every confidence is 0.25. At threshold 0, first-index mutual ties retain only `[[0,0]]`; at threshold 0.25 no match survives.
2. Mask the second target in that example: the first column confidence is `[0.5,0.5]` and the second column zero. Only `[[0,0]]` survives at threshold 0.

## Source and scope

[Primary source](https://arxiv.org/abs/2104.00680). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
