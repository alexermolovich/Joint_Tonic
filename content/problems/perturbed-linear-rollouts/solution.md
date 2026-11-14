# Solution

Add the supplied perturbations to nominal controls once. Allocate all states, initialize every candidate independently, and advance across time while vectorizing candidates. O(KH(D²+DU)) time and O(KH(D+U)) output memory.

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

def rollout_controls(initial,transition,control_map,nominal,perturbations):
    x=_array(initial,1);a=_array(transition,2);b=_array(control_map,2);u=_array(nominal,2);eps=_array(perturbations,3);d=len(x);h,c=u.shape
    if not 1<=d<=8 or not 1<=c<=8 or not 1<=h<=64 or not 1<=len(eps)<=128 or a.shape!=(d,d) or b.shape!=(d,c) or eps.shape[1:]!=u.shape:raise ValueError("rollout shape")
    if np.any(np.sum(np.abs(a),axis=1)>1) or np.any(np.abs(b)>10) or any(np.any(np.abs(z)>100) for z in (x,u,eps)):raise ValueError("bounded model")
    controls=u[None,:,:]+eps;states=np.empty((len(eps),h+1,d));states[:,0]=x
    for t in range(h):states[:,t+1]=states[:,t]@a.T+controls[:,t]@b.T
    return dict(states=states,controls=controls)
```
