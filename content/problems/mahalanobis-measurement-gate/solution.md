# Solution

Solve the shared system for residual columns, then reduce row products. O(D³+ND²) time and O(ND+D²) storage.

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

def _cov(value, n, positive=False):
    a=_real(value)
    if a.shape!=(n,n) or not np.allclose(a,a.T,rtol=0,atol=1e-10): raise ValueError("Invalid covariance shape or symmetry")
    a=(a+a.T)/2
    eig,vectors=np.linalg.eigh(a)
    if np.any(eig< -1e-10) or (positive and np.any(eig<=1e-10)): raise ValueError("Invalid covariance spectrum")
    return (vectors*np.maximum(eig,0))@vectors.T if np.any(eig<0) else a

def gate_measurements(residuals, covariance, threshold):
    r,t=map(_real,(residuals,threshold))
    if r.ndim!=2 or not 1<=r.shape[1]<=32 or t.ndim!=0 or t<0: raise ValueError("Invalid residual shape or threshold")
    S=_cov(covariance,r.shape[1],True)
    distances=np.maximum(np.einsum("ij,ij->i",r,np.linalg.solve(S,r.T).T),0)
    return distances,distances<=t
```
