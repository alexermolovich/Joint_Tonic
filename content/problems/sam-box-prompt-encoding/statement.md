# Encode a Box Prompt with Positional Features

Implement `encode_boxes(boxes: np.ndarray, image_size: tuple[int,int], frequencies: np.ndarray, corner_embeddings: np.ndarray) -> np.ndarray`.

Encode top-left and bottom-right box corners as distinct prompt tokens.
boxes is float64 (N,4) ordered (x1,y1,x2,y2),0<=N<=2048, with 0<=x1<=x2<=width-1 and 0<=y1<=y2<=height-1 in pixel-index coordinates. Degenerate equal corners are allowed. image_size tuple (height,width) uses positive built-in ints<=100000. frequencies float64 (2,F),1<=F<=128,absolute values<=100; corner_embeddings float64 (2,2F),row0 top-left,row1 bottom-right. For each corner add 0.5, divide by [width,height], map to [-1,1], form phase=2π*q@frequencies, concatenate sine then cosine channels and add that corner's vector. Return float64 (N,2,2F), preserving box and corner order. This encodes supplied boxes; it neither predicts boxes nor decodes masks.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. In image (1,1), box `[0,0,0,0]`, frequencies=`[[1],[0]]`, corner vectors `[[1,2],[3,4]]` gives `[[[1,3],[3,5]]]`.
2. In image (2,2), box `[0,0,1,1]`, frequencies=`[[0.5],[0]]`, zero corner vectors gives top-left `[-1,0]` and bottom-right `[1,0]`.

## Source and scope

[Primary source](https://arxiv.org/abs/2304.02643). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
