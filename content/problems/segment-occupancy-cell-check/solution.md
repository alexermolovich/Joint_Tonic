# Solution

Check every occupied cell with a two-axis slab intersection. O(HW) time, O(HW) occupied-index storage. The bounded grid keeps exhaustive checking practical.

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

def segment_is_free(grid, start, end):
    grid,a,b=map(_real,(grid,start,end))
    if grid.ndim!=2 or not all(1<=n<=128 for n in grid.shape) or np.any(~np.isin(grid,[0,1])) or a.shape!=(2,) or b.shape!=(2,): raise ValueError("Invalid map geometry")
    bounds=np.array([grid.shape[1],grid.shape[0]])
    if np.any(a<0) or np.any(b<0) or np.any(a>bounds) or np.any(b>bounds): raise ValueError("Endpoint outside map")
    direction=b-a
    for row,col in np.argwhere(grid==1):
        low=np.array([col,row]); high=low+1; enter,leave=0.,1.; possible=True
        for j in range(2):
            if direction[j]==0:
                if a[j]<low[j] or a[j]>high[j]: possible=False; break
            else:
                u=(low[j]-a[j])/direction[j]; v=(high[j]-a[j])/direction[j]
                enter=max(enter,min(u,v)); leave=min(leave,max(u,v))
                if enter>leave: possible=False; break
        if possible: return False
    return True
```
