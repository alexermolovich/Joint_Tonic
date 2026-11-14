# Solution

Transform source centers once, then broadcast pairwise differences in target pixels. Combine masks before emitting labels and replace unsupported distances with NaN. O(NM) time and memory.

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

def _homography(h):
    if h.shape[-2:]!=(3,3) or np.any(np.abs(h)>1000) or np.any(np.abs(np.linalg.det(h))<1e-9):raise ValueError("homography contract")
    return h

def _project(points,h):
    homogeneous=np.column_stack([points,np.ones(len(points))])@h.T;valid=np.abs(homogeneous[:,2])>1e-9
    uv=np.full((len(points),2),np.nan);uv[valid]=homogeneous[valid,:2]/homogeneous[valid,2,None]
    return uv,valid

def _size(size):
    size=_array(size,1,"i")
    if size.shape!=(2,) or np.any((size<1)|(size>4096)):raise ValueError("image size")
    return size

def _inside(p,size):
    return (p[:,0]>=0)&(p[:,0]<=size[1]-1)&(p[:,1]>=0)&(p[:,1]<=size[0]-1)

def descriptor_targets(source_centers,target_centers,target_from_source,source_valid,target_valid,tolerance):
    a=_array(source_centers,2);b=_array(target_centers,2);h=_array(target_from_source,2);ma=_array(source_valid,1,"b");mb=_array(target_valid,1,"b");tau=_scalar(tolerance,0,100)
    if a.shape[1]!=2 or b.shape[1]!=2 or len(a)>512 or len(b)>512 or h.shape!=(3,3) or ma.shape!=(len(a),) or mb.shape!=(len(b),):raise ValueError("correspondence contract")
    _homography(h);uv,valid=_project(a,h);supported=(ma&valid)[:,None]&mb[None,:];distance=np.linalg.norm(uv[:,None,:]-b[None,:,:],axis=2);distance=np.where(supported,distance,np.nan)
    return dict(distances=distance,correspondence=supported&(distance<=tau))
```
