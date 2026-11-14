# Worked code examples

The output is a list of original input indices in greedy selection order.

## Example 1: suppress a redundant same-class box

```python
from solution import class_aware_nms

boxes = [[0,0,10,10], [1,1,9,9], [20,20,30,30]]
print(class_aware_nms(boxes, [0.9,0.8,0.7], [0,0,0]))
```

Expected output:

```text
[0, 2]
```

Index 0 suppresses index 1 because their IoU is `0.64`. Index 2 is spatially separate.

## Example 2: different classes retain overlapping detections

```python
from solution import class_aware_nms

boxes = [[0,0,10,10], [0,0,10,10]]
print(class_aware_nms(boxes, [0.8,0.9], [0,1]))
```

Expected output:

```text
[1, 0]
```

Class-aware suppression preserves both boxes, while confidence still determines their global order.

## Example 3: identical boxes at the equality boundary

```python
from solution import class_aware_nms

boxes = [[0,0,10,10], [0,0,10,10]]
print(class_aware_nms(boxes, [0.8,0.9], [0,0], iou_threshold=1.0))
```

Expected output:

```text
[1, 0]
```

Their IoU equals the threshold. The contract suppresses only strictly greater overlap.
