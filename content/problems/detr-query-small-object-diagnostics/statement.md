# Diagnose Query Collapse and Missed Small Objects

Implement `diagnose_queries(features: np.ndarray, predicted_boxes: np.ndarray, target_boxes: np.ndarray, cosine_limit: float, iou_limit: float, small_area: float) -> dict`.

Report highly similar query pairs and geometrically uncovered small target boxes as separate diagnostics.
features float64(Q,D),0<=Q<=256,1<=D<=128, each row norm>=1e-8. predicted_boxes float64(Q,4) and target_boxes float64(M,4),0<=M<=256, normalized xyxy in [0,1] with strictly positive width/height. Scalars are built-in non-bool int/float: cosine_limit in [-1,1], iou_limit in (0,1], small_area in [0,1]. Return {"similar_pairs":int64(K,2),"missed_small_indices":int64(L,)}. Similar pairs are i<j with normalized feature dot product>=cosine_limit, sorted lexicographically. A small target has normalized area<=small_area and is missed if every prediction has IoU<iou_limit. With Q=0 all small targets are missed. No class labels or one-to-one matching are used: coverage is class-agnostic, and similar feature pairs flag potential redundancy rather than proving query collapse.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Features `[[1,0],[2,0]]` are identical directions. Predictions both box `[0,0,0.1,0.1]`; targets that box and `[0.8,0.8,0.9,0.9]`; limits (0.99,0.5,0.02) give similar_pairs=`[[0,1]]`, missed_small_indices=`[1]`.
2. With no queries and targets `[0,0,0.1,0.1]` and `[0,0,1,1]`, small_area=0.02 returns no pairs and missing index `[0]`. Large targets are outside this slice.

## Source and scope

[Primary source](https://arxiv.org/abs/2005.12872). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
