# Rank Candidate Masks with Predicted IoU

Implement rank_masks(masks, predicted_iou, k). masks is a NumPy bool array (N,H,W), 0<=N<=1024, 1<=H,W<=512, at most1,000,000 elements. predicted_iou is finite NumPy float64 (N,), absolute values<=1e6. These are learned quality scores: preserve raw values, including values outside[0,1], rather than clipping or recalibrating. k is a built-in int excluding bool in [0,N]. Sort by decreasing score; ties choose lower original candidate index. Return (selected_masks, indices, selected_scores), new arrays of shapes (k,H,W),(k,),(k,) and dtype bool,int64,float64. Preserve inputs and support noncontiguous arrays. Empty candidates require k=0 and return correctly shaped empties. TypeError for non-array arguments; ValueError for all other violations. Masks share one image pixel frame with row down and column right; each candidate is an alternative interpretation of the same prompt and exposure. No mask averaging, overlap suppression, ground-truth IoU calculation, thresholding logits, or geometric resizing. Predicted score is not a guarantee of mask correctness.

## Examples

## Keep the best interpretation

masks=[[[1,0]],[[0,1]],[[1,1]]] as bool, scores=[.7,.9,.8], k=2. Output masks=[[[0,1]],[[1,1]]], indices=[1,2], scores=[.9,.8]. Geometry follows each chosen index unchanged.

## Preserve score ties and raw quality

masks=[[[1]],[[0]],[[1]]] as bool, scores=[1.2,1.2,-.1], k=2. Output indices=[0,1], masks=[[[1]],[[0]]], scores=[1.2,1.2]. Lower input index breaks the tie; scores are not clipped to one.

## Hints

1. Stable descending sorting preserves original index order on ties.
2. Use the same chosen indices for masks and scores.
3. Keep raw scores; predicted quality is not ground-truth IoU.
