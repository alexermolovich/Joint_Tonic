# Solution

Validate dimensions and covariance spectra, then use matrix multiplication. O(n³) time, O(n²) storage. Symmetrization removes roundoff but does not repair invalid inputs.

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

def kalman_predict(x, P, F, Q):
    x,F=map(_real,(x,F))
    if x.ndim!=1 or not 1<=len(x)<=32 or F.shape!=(len(x),len(x)): raise ValueError("Invalid state shape")
    P,Q=_cov(P,len(x)),_cov(Q,len(x))
    covariance=F@P@F.T+Q
    return F@x,(covariance+covariance.T)/2
```
