# Solution: expose both box-set axes

Validate shape, finite real values, coordinate bounds, and non-reversed corners. Compute lower intersection corners with `maximum` and upper corners with `minimum` after inserting independent N/M axes. Clamp extents to zero **before** taking the product.

```python
lo = np.maximum(a[:, None, :2], b[None, :, :2])
hi = np.minimum(a[:, None, 2:], b[None, :, 2:])
intersection = np.prod(np.maximum(hi - lo, 0), axis=-1)
```

Compute each set's area once, broadcast them into union, and use `np.divide(intersection, union, out=zeros, where=union>0)`. This defines zero-union values without introducing a small arbitrary epsilon that would bias valid scores.

Time and output memory are O(NM). Temporary corner arrays are also O(NM). A blocked implementation can reduce temporary memory for a large N/M while preserving the same final matrix. The current bounded problem allows the direct vectorized method.
