# Monitor Frozen-Feature Drift Across Camera Domains

Implement `feature_drift(reference: np.ndarray, current: np.ndarray) -> tuple[np.ndarray, float]`.

Compare frozen-feature channel means using a reference-domain scale.
Inputs reference (N,D) and current (M,D) float64 contain dimensionless embeddings from the SAME frozen encoder/preprocessing,1<=N,M<=4096,1<=D<=256. Compute population reference variance (divide by N), then per-channel shift `z=(mean(current)-mean(reference))/sqrt(var(reference)+1e-6)`. Return fresh float64(D,) z and Python float score sqrt(mean(z**2)). No normalization of individual embeddings, covariance estimate, model update, thresholding, or causal diagnosis occurs. A single reference sample is valid with zero variance. Comparing different encoder versions is outside the contract.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. reference=`[[0],[2]]`, current=`[[1],[3]]`: z=`[1/√1.000001]` and score=1/√1.000001. The reference mean is 1 and current mean is 2.
2. Identical constant clouds `[[4,4]]` have zero shift and score 0. Changing one current channel to 4.001 gives z≈`[1,0]`, score≈1/√2 because the variance floor is 1e-6.

## Source and scope

[Primary source](https://arxiv.org/abs/2304.07193). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
