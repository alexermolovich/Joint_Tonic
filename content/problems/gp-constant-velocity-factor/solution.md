# Solution

Construct the physical residual before whitening. Solve with a lower Cholesky factor, never with the covariance itself: the squared residual norm must equal the inverse-covariance quadratic form. O(D) time and output memory because every factor is 2×2.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int, float) or not low <= x <= high or not np.isfinite(x):
        raise ValueError("Scalar outside contract")
    return float(x)

def gp_motion_factor(start,end,duration,spectral_density):
    a=_array(start,2);b=_array(end,2);qc=_array(spectral_density,1);t=_scalar(duration,1e-3,100)
    if not 1<=len(a)<=16 or a.shape[1]!=2 or b.shape!=a.shape or qc.shape!=(len(a),) or np.any(qc<1e-6):raise ValueError("support state contract")
    e=b-a;e[:,0]-=t*a[:,1]
    q=qc[:,None,None]*np.array([[t**3/3,t*t/2],[t*t/2,t]])
    white=np.linalg.solve(np.linalg.cholesky(q),e[...,None])[...,0]
    return dict(residual=e,covariance=q,whitened=white,cost=float(.5*np.sum(white*white)))
```
