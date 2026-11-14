# Solution

Find runs in O(N), reject repeated run labels, enumerate complete windows in O(Kw) time and output memory.

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

def episode_windows(episode_ids, window, stride):
    ids=_real(episode_ids)
    if ids.ndim!=1 or np.any(ids<0) or np.any(ids!=np.floor(ids)): raise ValueError("Invalid IDs")
    for n in (window,stride):
        if isinstance(n,(bool,np.bool_)) or not isinstance(n,(int,np.integer)) or not 1<=n<=10000: raise ValueError("Invalid width or stride")
    if not len(ids): return np.empty((0,window),dtype=np.int64)
    bounds=np.r_[0,np.flatnonzero(np.diff(ids)!=0)+1,len(ids)]
    labels=ids[bounds[:-1]]
    if len(set(labels))!=len(labels): raise ValueError("Episode ID reappeared")
    starts=[s for a,b in zip(bounds[:-1],bounds[1:]) for s in range(int(a),int(b)-window+1,stride)]
    return np.asarray(starts,dtype=np.int64)[:,None]+np.arange(window,dtype=np.int64)[None,:]
```
