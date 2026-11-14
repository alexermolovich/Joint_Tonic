# Detect Prompt and Class Distribution Drift

Implement `prompt_class_drift(old_prototypes: np.ndarray, new_prototypes: np.ndarray, old_counts: np.ndarray, new_counts: np.ndarray) -> tuple[np.ndarray, float]`.

Separate changed text prototypes from changed predicted-class frequencies.
old_prototypes and new_prototypes are float64(C,D),1<=C<=256,1<=D<=512; each row norm>=1e-8. Rows refer to the same ordered classes and same encoder version. old_counts,new_counts are int64(C,) nonnegative<=1000000, each with positive total. Return float64(C,) cosine distances `1-dot(normalize(old),normalize(new))`, clipped into [0,2], and Python float Jensen-Shannon divergence between normalized count histograms, using natural logs and 0*log(0)=0. Counts describe comparable observation windows, not necessarily equal sample counts. No pseudocount smoothing, class remapping, or causal attribution. Changing class inventory requires a new contract upstream.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Old prototypes `[[1,0],[0,1]]`, new `[[1,0],[1,0]]` give distances `[0,1]`. Counts `[1,0]` versus `[0,1]` give JS=ln(2).
2. Multiplying every prototype by a positive scale and counts `[1,3]` to `[2,6]` gives zero drift in both outputs: directions and proportions are unchanged.

## Source and scope

[Primary source](https://arxiv.org/abs/2103.00020). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
