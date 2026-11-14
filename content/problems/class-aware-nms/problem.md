# Run Class-Aware Non-Maximum Suppression

Several boxes can describe the same object. Implement `class_aware_nms(boxes, scores, class_ids, iou_threshold=0.5)` to keep confident detections and remove redundant boxes of the **same** class.

## Contract

- `boxes`: finite real numeric `(N,4)` array-like of continuous image-space `[x1,y1,x2,y2]`, with coordinate magnitude <=1e6 and non-reversed corners. Zero-area boxes are allowed.
- `scores`: finite real `(N,)` array-like in `[0,1]`.
- `class_ids`: nonnegative integer-valued `(N,)` array-like. Integral float values are accepted. Booleans are invalid. Class IDs are at most `2**31-1`.
- `iou_threshold`: finite real scalar in `[0,1]`.

Sort by descending score; ties prefer the **lower original input index**. Keep the first remaining box. Suppress any remaining candidate only when its class matches the kept box and their IoU is **strictly greater** than the threshold. Repeat with the remaining list. A suppressed box never suppresses another box.

Return a list of Python integer indices into the original input, in the order boxes were kept. Use continuous areas without +1; zero-area boxes have IoU zero. An empty `(0,4)` array with two empty vectors returns `[]`. Raise `ValueError` for any malformed shape, range, type, or nonfinite value. Preserve all inputs.

## Example 1: one redundant detection

```python
boxes = [[0,0,10,10], [1,1,9,9], [20,20,30,30]]
scores = [.9,.8,.7]
class_ids = [0,0,0]
# [0,2]
```

The first pair has IoU `.64`, so index 1 is suppressed at the default `.5` threshold. The third box is separate.

## Example 2: overlap across classes

```python
boxes = [[0,0,10,10], [0,0,10,10]]
scores = [.8,.9]
class_ids = [0,1]
# [1,0]
```

Both survive because classes differ. Score order still puts index 1 first. If their classes match and `iou_threshold=1.0`, both also survive because IoU equality does not trigger suppression.

## Constraints and hints

`0<=N<=2_000`. A greedy loop over selected candidates is expected; vectorize overlap against the remaining candidates. Once a box is suppressed, remove it from the candidate list before the next step. Use a stable sort to preserve original-index tie order.
