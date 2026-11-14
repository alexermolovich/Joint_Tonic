# Solution

Accumulate angles and link vectors. O(N) time and output memory. No simulator is required for deterministic grading.

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

def planar_forward_kinematics(lengths, q):
    lengths,q=map(_real,(lengths,q))
    if lengths.ndim!=1 or not 1<=len(lengths)<=1000 or q.shape!=lengths.shape or np.any(lengths<=0): raise ValueError("Invalid serial chain")
    theta=np.cumsum(q); directions=np.column_stack([np.cos(theta),np.sin(theta)])
    origins=np.vstack([np.zeros(2),np.cumsum(lengths[:,None]*directions,axis=0)])
    c,s=np.cos(theta[-1]),np.sin(theta[-1]); T=np.array([[c,-s,origins[-1,0]],[s,c,origins[-1,1]],[0.,0.,1.]])
    return origins,T
```
