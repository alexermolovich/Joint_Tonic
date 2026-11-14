# Build a Detection Bipartite-Matching Cost Matrix

**Status: drafted; not runnable yet.**

Build pairwise query-to-target costs from class probabilities, normalized box distances, and generalized IoU.

```python
def detr_matching_cost(class_probs: np.ndarray, pred_boxes: np.ndarray,
                       target_labels: np.ndarray, target_boxes: np.ndarray,
                       weights: tuple[float, float, float] = (1.0, 5.0, 2.0)) -> np.ndarray:
```

## Contract

Implement the cost construction used before one-to-one matching. Return the entire matrix; do not run the Hungarian algorithm or compute a training loss.

| Argument | Required contract |
|---|---|
| `class_probs` | NumPy `float64`, shape `(Q,K+1)`, `1 <= Q <= 300`, `1 <= K <= 1000`. Finite entries in `[0,1]`; each row sums to one within absolute tolerance `1e-6`. The final column is no-object. |
| `pred_boxes` | NumPy `float64`, shape `(Q,4)`, finite normalized `(cx,cy,w,h)`. Centers in `[0,1]`, sizes in `[1e-6,1]`. The minimum size is a teaching bound preventing corner collapse in float64. Corners may extend outside the image; do not clip. |
| `target_labels` | NumPy `int64`, shape `(M,)`, `0 <= M <= Q`, each in `[0,K-1]`. No no-object targets. Repeated labels are valid. |
| `target_boxes` | NumPy `float64`, shape `(M,4)`, same box rules as predictions. |
| `weights` | A tuple of three finite Python `int`/`float` values, excluding booleans: class, L1, GIoU weights. Each in `[0,100]`, at least one positive. |

For query `i`, target `j`, use `-w_class * class_probs[i,target_labels[j]] + w_l1 * sum(abs(pred_boxes[i]-target_boxes[j])) - w_giou * GIoU(i,j)`. L1 uses center/size coordinates; GIoU uses corners. The sign and constant matter: this exercise requires **negative GIoU**, not `1-GIoU`.

Return a newly allocated `float64` array `(Q,M)`, with queries as rows and targets as columns. Inputs remain unchanged; output does not alias them. Empty targets produce `(Q,0)` after validating all inputs. There are no timestamp or physical-distance inputs.

Raise `TypeError` if one of the four array arguments is not a NumPy array. Raise `ValueError` for every other contract violation, including wrong dtype, invalid weights, shape, NaN/Inf, out-of-range box size, or a background target. Validate before computing. Test inputs have at most one violation, so error precedence is not graded.

## Example 1: two competing queries

```python
class_probs = np.array([[0.8, 0.1, 0.1], [0.2, 0.7, 0.1]], dtype=np.float64)
pred_boxes = np.array([[0.25, 0.5, 0.5, 1.0], [0.75, 0.5, 0.5, 1.0]], dtype=np.float64)
target_labels = np.array([0, 1], dtype=np.int64)
target_boxes = pred_boxes.copy()
detr_matching_cost(class_probs, pred_boxes, target_labels, target_boxes, (1.0, 1.0, 1.0))
# array([[-1.8,  0.4],
#        [ 0.3, -1.7]])
```

Identical boxes have GIoU `1` and L1 `0`. The two different boxes touch, have GIoU `0`, and center/size L1 distance `0.5`. The diagonal is inexpensive, but this function does not choose an assignment.

## Example 2: disjoint boxes still have a geometry cost

```python
class_probs = np.array([[0.6, 0.4]], dtype=np.float64)
pred_boxes = np.array([[0.25, 0.5, 0.2, 0.2]], dtype=np.float64)
target_labels = np.array([0], dtype=np.int64)
target_boxes = np.array([[0.75, 0.5, 0.2, 0.2]], dtype=np.float64)
detr_matching_cost(class_probs, pred_boxes, target_labels, target_boxes, (1.0, 1.0, 1.0))
# array([[0.3285714285714286]])
```

Intersection is `0`, union is `0.08`, and enclosing rectangle area is `0.14`. GIoU is `-3/7`, so the cost is `-0.6 + 0.5 + 3/7`. Outputs are compared numerically, not by printed decimal formatting.

## Planned evaluation budget

Python 3.12.3, CPU, numpy 2.2.4. Proposed limit: 3 seconds wall time, 2 seconds CPU time, 512 MiB memory, 64 KiB output. Image packaging and budget calibration are pending; this draft is not executable in the application.
