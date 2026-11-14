# Solution

Validate the grid and observation table, copy the grid, and update rows sequentially. O(HW+N) time, O(HW) output storage.

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

def update_occupancy(log_odds, observations, prior, limit):
    grid,obs,p,b=map(_real,(log_odds,observations,prior,limit))
    if grid.ndim!=2 or min(grid.shape)<1 or obs.ndim!=2 or obs.shape[1]!=3 or p.ndim!=0 or not 0<p<1 or b.ndim!=0 or b<=0 or np.any(np.abs(grid)>b): raise ValueError("Invalid map contract")
    indices=obs[:,:2]
    if np.any(indices!=np.floor(indices)) or np.any(indices<0) or np.any(indices[:,0]>=grid.shape[0]) or np.any(indices[:,1]>=grid.shape[1]) or np.any(obs[:,2]<=0) or np.any(obs[:,2]>=1): raise ValueError("Invalid observation")
    out=grid.copy(); prior_logit=np.log(p)-np.log1p(-p)
    for row,col,prob in obs:
        i,j=int(row),int(col)
        out[i,j]=np.clip(out[i,j]+np.log(prob)-np.log1p(-prob)-prior_logit,-b,b)
    return out
```
