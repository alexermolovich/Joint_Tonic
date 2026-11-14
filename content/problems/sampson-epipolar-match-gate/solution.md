# Solution

Rescale F safely, check the declared rank policy, then form both epipolar-line batches and their sensitivity denominators. O(N) arithmetic and memory beyond the fixed 3x3 SVD. Mask unsupported denominators before division.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x,low,high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def epipolar_gate(source,target,fundamental,valid,threshold):
    a=_array(source,2);b=_array(target,2);f=_array(fundamental,2);mask=_array(valid,1,"b");tau=_scalar(threshold,0,100)
    if a.shape[1]!=2 or b.shape!=a.shape or len(a)>16384 or f.shape!=(3,3) or mask.shape!=(len(a),):raise ValueError("epipolar contract")
    scale=np.max(np.abs(f))
    if scale==0:raise ValueError("zero fundamental matrix")
    f=f/scale;f=f/np.linalg.norm(f);singular=np.linalg.svd(f,compute_uv=False)
    if singular[1]<=1e-8 or singular[2]>1e-8:raise ValueError("numerical rank-two fundamental matrix required")
    ah=np.column_stack([a,np.ones(len(a))]);bh=np.column_stack([b,np.ones(len(b))]);line_b=ah@f.T;line_a=bh@f;residual=np.sum(bh*line_b,axis=1);den=np.sum(line_b[:,:2]**2,axis=1)+np.sum(line_a[:,:2]**2,axis=1);supported=mask&(den>1e-12);error=np.divide(residual**2,den,out=np.full(len(a),np.inf),where=supported)
    return dict(squared_error=error,accepted=supported&(error<=tau*tau))
```
