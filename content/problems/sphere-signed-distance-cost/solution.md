# Solution

O(BSK) time and memory. Evaluate sphere-pair clearances before reducing cost, minimum clearance, and collision; each reduction has a different meaning.

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

def sphere_collision_cost(centers,radii,obstacles,obstacle_radii,margin):
    c=_array(centers,3);r=_array(radii,1);o=_array(obstacles,2);s=_array(obstacle_radii,1);m=_scalar(margin,0,100)
    b,n,xyz=c.shape;k=len(o)
    if not 1<=b<=64 or not 1<=n<=32 or xyz!=3 or not 1<=k<=32 or o.shape!=(k,3) or r.shape!=(n,) or s.shape!=(k,) or np.any(r<1e-9) or np.any(s<1e-9):raise ValueError("sphere contract")
    d=np.linalg.norm(c[:,:,None,:]-o[None,None,:,:],axis=-1)-r[None,:,None]-s[None,None,:]
    return dict(cost=np.sum(np.maximum(m-d,0)**2,axis=(1,2)),clearance=np.min(d,axis=(1,2)),collision=np.any(d<=0,axis=(1,2)))
```
