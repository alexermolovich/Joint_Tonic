# Worked code examples

This decoder uses direct image-relative widths/heights and per-box class probabilities. The displayed confidence is rounded for readability.

## Example 1: a single grid cell

```python
import numpy as np
from solution import decode_yolo

p = np.array([[[[0.5,0.5,0.4,0.5,0.8,0.75]]]])
out = decode_yolo(p, (100,80))
print([(r['box'], r['class_id'], round(r['score'], 3)) for r in out])
```

Expected output:

```text
[([30.0, 20.0, 70.0, 60.0], 0, 0.6)]
```

The center is `(50,40)`, the size is `(40,40)` pixels, and confidence is `0.8 × 0.75`.

## Example 2: one box can produce two classes

```python
import numpy as np
from solution import decode_yolo

p = np.array([[[[0.5,0.5,0.4,0.5,0.8,0.75,0.5]]]])
out = decode_yolo(p, (100,80), score_threshold=0.4)
print([(r['class_id'], round(r['score'], 3)) for r in out])
```

Expected output:

```text
[(0, 0.6), (1, 0.4)]
```

The threshold is inclusive. A class score equal to `0.4` survives; an argmax-only decoder would lose that required candidate.

## Example 3: low confidence produces a valid empty result

```python
import numpy as np
from solution import decode_yolo

p = np.array([[[[0.5,0.5,0.4,0.5,0.2,0.75]]]])
print(decode_yolo(p, (100,80)))
```

Expected output:

```text
[]
```

The geometry is well formed, but its confidence product is below the default cutoff.
