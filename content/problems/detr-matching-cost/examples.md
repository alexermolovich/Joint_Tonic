# Worked examples

These original synthetic examples are public teaching material, not hidden evaluator fixtures. The [statement](#) is the complete contract.

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

## Theory question answers

1. Every pair cost gains the same GIoU weight, so the exact matrix changes but fixed-cardinality assignment ordering does not.
2. Several queries may choose the same target; the later assignment solver must enforce uniqueness.
