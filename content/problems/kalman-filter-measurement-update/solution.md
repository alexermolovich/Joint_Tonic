# Solution

Solve the positive-definite innovation system and evaluate the Joseph form. O(n³+m³+n²m+nm²) time and O(n²+m²+nm) storage for dense matrices.

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

def kalman_update(x, P, z, H, R):
    x,z,H=map(_real,(x,z,H))
    if x.ndim!=1 or z.ndim!=1 or not 1<=len(x)<=32 or not 1<=len(z)<=32 or H.shape!=(len(z),len(x)): raise ValueError("Invalid state or observation shape")
    P,R=_cov(P,len(x)),_cov(R,len(z),True)
    S=H@P@H.T+R; K=np.linalg.solve(S,H@P).T
    A=np.eye(len(x))-K@H; covariance=A@P@A.T+K@R@K.T
    return x+K@(z-H@x),(covariance+covariance.T)/2
```
