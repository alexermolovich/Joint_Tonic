# Solution

Normalize each metric using the stated PSD rule, sum natural forces and metrics, and resolve only retained eigenvectors of the combined metric. O(KD³+D³) time including validation and O(KD²) temporary memory.

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

def _metric(m):
    if not np.allclose(m,m.swapaxes(-1,-2),atol=1e-10,rtol=0):raise ValueError("metric symmetry")
    eigen,vectors=np.linalg.eigh(.5*(m+m.swapaxes(-1,-2)))
    if np.any(eigen < -1e-10):raise ValueError("metric positivity")
    return (vectors*np.maximum(eigen,0)[...,None,:])@vectors.swapaxes(-1,-2)

def combine_policies(metrics,accelerations):
    m=_array(metrics,3);a=_array(accelerations,2);k,d,_=m.shape
    if not 1<=k<=64 or not 1<=d<=16 or m.shape[2]!=d or a.shape!=(k,d):raise ValueError("common policy shape")
    effective=_metric(m);total=effective.sum(axis=0);force=np.einsum('kij,kj->i',effective,a)
    eigen,vectors=np.linalg.eigh(total);keep=eigen>1e-10*max(float(eigen[-1]),0.)
    acceleration=vectors[:,keep]@((vectors[:,keep].T@force)/eigen[keep])
    return dict(metric=total,force=force,acceleration=acceleration,rank=int(keep.sum()))
```
