# Decode Phrase-Labeled Boxes

Implement `decode_grounded_boxes(boxes: np.ndarray, token_logits: np.ndarray, phrase_map: np.ndarray, image_size: tuple[int,int], threshold: float) -> dict`.

Associate each normalized box with its strongest phrase, then return thresholded pixel boxes.
boxes float64 (Q,4) contains normalized image (cx,cy,width,height), all values in [0,1], positive width/height;0<=Q<=2048. token_logits float64 (Q,T),1<=T<=512. phrase_map bool (P,T),1<=P<=128; every phrase must have at least one token. image_size is tuple (height,width) built-in positive ints<=100000. threshold is built-in non-bool int/float in [0,1]. Sigmoid each token logit stably. A phrase score is MAX probability over its mapped tokens (a declared teaching aggregation); choose highest phrase per query, ties lower phrase index. Keep score>=threshold in original query order. Return exactly query_indices int64(K,), phrase_indices int64(K,), scores float64(K,), boxes_xyxy float64(K,4). Convert normalized center-size to pixel corners without clipping; boxes can extend outside the image. No NMS or tokenizer runs.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Box `[0.5,0.5,0.5,1]`, two zero logits, phrase_map=I₂ bool, image (100,200), threshold=0.5 yields query0, phrase0 (tie), score0.5, corners `[50,0,150,100]`.
2. Box `[0,0,1,1]`, one logit0, one phrase, image (10,20), threshold=0.5 yields `[-10,-5,10,5]`. Coordinates remain unclipped.

## Source and scope

[Primary source](https://arxiv.org/abs/2303.05499). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
