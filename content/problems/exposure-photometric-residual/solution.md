# Solution

Compute the source-to-target brightness ratio, subtract the corrected source intensity, and evaluate the documented Huber value and target derivative. O(N) time and memory.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def photometric_residual(source,target,exposures,log_gains,offsets,weights,huber_delta):
    a=_array(source,1);b=_array(target,1);t=_array(exposures,1);g=_array(log_gains,1);o=_array(offsets,1);w=_array(weights,1);delta=_scalar(huber_delta,1e-6,1)
    if len(a)>65536 or b.shape!=a.shape or w.shape!=a.shape or t.shape!=(2,) or g.shape!=(2,) or o.shape!=(2,) or any(np.any((x<0)|(x>1)) for x in (a,b,w)) or np.any((t<1e-6)|(t>1)) or np.any(np.abs(g)>10) or np.any(np.abs(o)>1):raise ValueError("photometric contract")
    ratio=(t[1]/t[0])*np.exp(g[1]-g[0]);r=(b-o[1])-ratio*(a-o[0]);absr=np.abs(r);energy=w*np.where(absr<=delta,.5*r*r,delta*(absr-.5*delta))
    return dict(residual=r,energy=energy,total=float(energy.sum()),target_gradient=w*np.clip(r,-delta,delta))
```
