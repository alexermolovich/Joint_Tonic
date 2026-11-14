# Compute Pairwise Bounding-Box IoU

A detector and an annotation system may produce different numbers of boxes. Implement `pairwise_iou(boxes_a, boxes_b)` to compare **every** box in the first set with **every** box in the second.

## Contract

- `boxes_a`: finite real numeric `(N,4)` array-like.
- `boxes_b`: finite real numeric `(M,4)` array-like.
- Each row is continuous image-space `[x1,y1,x2,y2]` in pixels, x right and y down. Both sets describe the same image. Coordinates may be negative; each magnitude must be at most `1e6`.
- Require `x2>=x1` and `y2>=y1`; reversed boxes raise `ValueError`.
- Return a new float64 `(N,M)` NumPy array, where row i / column j compares the corresponding pair. All scores lie in `[0,1]`.
- Width is `x2-x1`; there is **no pixel-inclusive +1**. Touching edges do not overlap. Zero-area boxes are allowed and always have IoU zero, including against another zero-area box.
- Support `(0,4)` inputs and preserve the resulting `(0,M)` or `(N,0)` shape. Do not mutate inputs.

Raise `ValueError` for invalid shape, nonfinite/complex numbers, out-of-range coordinates, or reversed boxes. Use NumPy broadcasting instead of Python loops over box pairs.

## Example 1: identity and separation

```python
boxes_a = [[0,0,2,2]]
boxes_b = [[0,0,2,2], [3,3,4,4]]
# array([[1., 0.]])
```

## Example 2: partial overlap and containment

```python
boxes_a = [[0,0,2,2]]
boxes_b = [[1,1,3,3], [0,0,1,1]]
# array([[1/7, 1/4]])
```

The first pair has intersection area 1 and union area 7. The second's small box is contained inside the larger box, so intersection/union is 1/4.

## Constraints and hints

`0<=N,M<=2_000`. Insert a singleton axis for the other set before computing maximum lower corners and minimum upper corners. Use a masked division to define zero-union results explicitly.
