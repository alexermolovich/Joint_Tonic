# Worked code examples

Scores below use continuous rectangle areas. The snippets round printed values only; the returned array should keep its numerical precision.

## Example 1: identical and disjoint boxes

```python
from solution import pairwise_iou

scores = pairwise_iou([[0,0,2,2]], [[0,0,2,2], [3,3,4,4]])
print(scores.tolist())
print(scores.shape)
```

Expected output:

```text
[[1.0, 0.0]]
(1, 2)
```

One predicted box is compared with two candidates, producing two columns.

## Example 2: partial overlap and containment

```python
import numpy as np
from solution import pairwise_iou

scores = pairwise_iou([[0,0,2,2]], [[1,1,3,3], [0,0,1,1]])
print(np.round(scores, 6).tolist())
```

Expected output:

```text
[[0.142857, 0.25]]
```

For the first pair, intersection is 1 and union is 7. For the second, the unit square occupies one quarter of the larger box.

## Example 3: a zero-area box

```python
from solution import pairwise_iou

print(pairwise_iou([[1,1,1,2]], [[1,1,1,2], [0,0,3,3]]).tolist())
```

Expected output:

```text
[[0.0, 0.0]]
```

A zero-width box has no area. Even a comparison with itself is defined as zero by this exercise.
