# Solution

Compute pairwise interval intersections by broadcast maxima/minima. O(PT) time/output storage.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def phrase_token_map(token_offsets, phrase_spans, text_length):
    t=_array(token_offsets,2,"i");p=_array(phrase_spans,2,"i")
    if t.shape[1:]!=(2,) or p.shape[1:]!=(2,) or len(t)>4096 or len(p)>4096 or type(text_length) is not int or not 0<=text_length<=1000000:raise ValueError("Offset shape")
    for a,strict in ((t,False),(p,True)):
        if np.any(a<0) or np.any(a>text_length) or np.any(a[:,0]>a[:,1]) or (strict and np.any(a[:,0]==a[:,1])):raise ValueError("Span bounds")
    return np.maximum(p[:,None,0],t[None,:,0])<np.minimum(p[:,None,1],t[None,:,1])
```
