# Select Language-Guided Object Queries

Implement `select_grounded_queries(scores: np.ndarray, usable_tokens: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]`.

Select visual queries by their strongest usable text-token compatibility.
scores float64 (Q,T) contains logits or unnormalized similarities,0<=Q<=4096,1<=T<=512; usable_tokens bool(T,) excludes padding and special tokens. k is built-in int non-bool with 0<=k<=Q. If k>0 at least one token must be usable. Rank each query by max score across usable tokens; sort descending, tie smaller query index. Return int64(k,) query indices and corresponding float64(k,) rank scores in that order. k=0 returns empty arrays even with no usable tokens. No softmax, sigmoid, NMS or decoder is run; supplied scores already follow the model's feature enhancement stage.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. scores=`[[1,100,3],[4,0,2],[4,9,1]]`, usable=`[True,False,True]`, k=2 gives indices `[1,2]`, scores `[4,4]`. The masked score 100 cannot win.
2. scores=`[[-3,-1],[-2,-4]]`, all tokens usable, k=1 gives index `[0]`, score `[-1]`. Negative logits remain valid evidence.

## Source and scope

[Primary source](https://arxiv.org/abs/2303.05499). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
