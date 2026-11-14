# Solution

Vector cross products construct each column in O(N) time and output memory.

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

def geometric_jacobian(origins, axes, joint_types, tool):
    o,z,p=map(_real,(origins,axes,tool))
    if o.ndim!=2 or o.shape[1]!=3 or not 1<=len(o)<=1000 or z.shape!=o.shape or p.shape!=(3,) or not isinstance(joint_types,(list,tuple)) or len(joint_types)!=len(o) or any(not isinstance(t,str) or t not in ("R","P") for t in joint_types) or np.any(np.abs(np.linalg.norm(z,axis=1)-1)>1e-7): raise ValueError("Invalid joint geometry")
    rev=np.array([t=="R" for t in joint_types]); linear=z.copy(); angular=np.zeros_like(z)
    linear[rev]=np.cross(z[rev],p-o[rev]); angular[rev]=z[rev]
    return np.concatenate([linear,angular],axis=1).T.copy()
```
