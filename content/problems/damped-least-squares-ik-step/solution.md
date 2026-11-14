# Solution

Use a thin SVD and singular-value filter. O(MN min(M,N)) time and O(MN) storage.

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

def damped_ik_step(jacobian, error, damping):
    J,e,d=map(_real,(jacobian,error,damping))
    if J.ndim!=2 or not all(1<=n<=32 for n in J.shape) or e.shape!=(J.shape[0],) or d.ndim!=0 or d<1e-9: raise ValueError("Invalid damped IK contract")
    U,s,Vt=np.linalg.svd(J,full_matrices=False); gain=s/(s*s+d*d)
    correction=Vt.T@(gain*(U.T@e))
    return correction,J@correction-e
```
