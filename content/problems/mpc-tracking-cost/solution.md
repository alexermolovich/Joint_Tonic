# Solution

Validate aligned horizon shapes, square tracking/control values, weight, and sum. O(N(D+M)) time with vectorized temporary arrays.

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

def mpc_tracking_cost(states, targets, controls, state_weights, control_weights, terminal_weights):
    x,r,u,q,s,p=map(_real,(states,targets,controls,state_weights,control_weights,terminal_weights))
    if x.ndim!=2 or min(x.shape)<1 or r.shape!=x.shape or u.ndim!=2 or u.shape[0]!=len(x)-1 or u.shape[1]<1 or q.shape!=(x.shape[1],) or p.shape!=q.shape or s.shape!=(u.shape[1],) or any(np.any(w<0) for w in (q,s,p)): raise ValueError("Invalid horizon contract")
    error=x-r
    return float(np.sum(error[:-1]**2*q)+np.sum(u**2*s)+np.sum(error[-1]**2*p))
```
