# Solution

Binary-search queries and broadcast interpolation over joints. O(M log T + MD) time and O(MD) output memory.

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

def sample_trajectory(times, positions, queries):
    t,q,s=map(_real,(times,positions,queries))
    if t.ndim!=1 or len(t)<2 or np.any(np.diff(t)<1e-9) or q.ndim!=2 or q.shape[0]!=len(t) or q.shape[1]<1 or s.ndim!=1 or np.any(s<t[0]) or np.any(s>t[-1]): raise ValueError("Invalid trajectory")
    k=np.clip(np.searchsorted(t,s,side="right")-1,0,len(t)-2)
    dt=t[k+1]-t[k]; velocity=(q[k+1]-q[k])/dt[:,None]
    return q[k]+(s-t[k])[:,None]*velocity,velocity
```
