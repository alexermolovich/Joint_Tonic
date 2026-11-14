# Solution

Build token validity with broadcasting and combine both axes with a lower-triangular boolean matrix. O(BT²) time/output storage.

```python
import numpy as np

def _real(value):
    try:
        a = np.asarray(value)
        if a.dtype.kind not in "iuf": raise ValueError("Expected real numeric data")
        a = a.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(a).all() or np.any(np.abs(a)>1e9):
        raise ValueError("Values must be finite with magnitude <=1e9")
    return a

def sequence_masks(lengths, max_steps):
    lengths=_real(lengths)
    if isinstance(max_steps,(bool,np.bool_)) or not isinstance(max_steps,(int,np.integer)) or not 0<=max_steps<=512: raise ValueError("Invalid T")
    if lengths.ndim!=1 or len(lengths)>128 or np.any(lengths<0) or np.any(lengths>max_steps) or np.any(lengths!=np.floor(lengths)): raise ValueError("Invalid lengths")
    t=np.arange(max_steps); valid=t[None,:]<lengths[:,None]
    attention=valid[:,:,None]&valid[:,None,:]&(t[None,:]<=t[:,None])[None,:,:]
    return valid,attention
```
