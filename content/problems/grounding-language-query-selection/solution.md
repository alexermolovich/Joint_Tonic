# Solution

Compute usable-token maxima and stable descending query ranking. O(QT+Q log Q) time.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def select_grounded_queries(scores, usable_tokens, k):
    s=_array(scores,2);v=_array(usable_tokens,1,"b")
    if len(s)>4096 or not 1<=s.shape[1]<=512 or v.shape!=(s.shape[1],) or type(k) is not int or not 0<=k<=len(s) or (k>0 and not v.any()):raise ValueError("Selection contract")
    if k==0:return np.empty(0,dtype=np.int64),np.empty(0,dtype=np.float64)
    rank=s[:,v].max(1);idx=np.lexsort((np.arange(len(s)),-rank))[:k]
    return idx.astype(np.int64),rank[idx]
```
