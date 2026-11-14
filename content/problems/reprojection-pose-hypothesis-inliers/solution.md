# Solution

Project each pose hypothesis independently, fill unsupported errors with infinity, and compute evidence counts and inlier-only medians. O(KN) projection work with O(KN) output storage; median computation has the usual selection cost.

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

def _rotation(r):
    if r.shape[-2:]!=(3,3) or not np.allclose(r.swapaxes(-1,-2)@r,np.eye(3),atol=1e-9,rtol=0) or not np.allclose(np.linalg.det(r),1,atol=1e-9,rtol=0):raise ValueError("proper rotation required")
    return r

def _transform(t):
    if t.shape[-2:]!=(4,4) or not np.allclose(t[...,3,:],[0,0,0,1],atol=1e-9,rtol=0):raise ValueError("rigid transform required")
    _rotation(t[...,:3,:3]);return t

def _intrinsics(k):
    if k.shape!=(4,) or np.any(k[:2]<1e-3):raise ValueError("camera intrinsics contract")
    return k

def pose_inliers(world_points,pixels,camera_from_world,intrinsics,pixel_std,valid,threshold):
    p=_array(world_points,2);uv=_array(pixels,2);t=_array(camera_from_world,3);k=_array(intrinsics,1);std=_array(pixel_std,1);mask=_array(valid,1,"b");limit=_scalar(threshold,0,100);n=len(p);count=len(t)
    if p.shape!=(n,3) or uv.shape!=(n,2) or n>4096 or not 1<=count<=64 or count*n>262144 or t.shape!=(count,4,4) or std.shape!=(n,) or mask.shape!=(n,) or np.any((std<1e-3)|(std>100)):raise ValueError("pose inlier contract")
    _transform(t);_intrinsics(k);errors=np.full((count,n),np.inf)
    for i in range(count):
        camera=p@t[i,:3,:3].T+t[i,:3,3];supported=mask&(camera[:,2]>1e-6);projected=camera[supported,:2]/camera[supported,2,None]*k[:2]+k[2:];errors[i,supported]=np.sum((projected-uv[supported])**2,axis=1)/std[supported]**2
    inliers=errors<=limit;counts=inliers.sum(axis=1,dtype=np.int64);median=np.array([np.median(errors[i,inliers[i]]) if counts[i] else np.nan for i in range(count)]);ids=np.flatnonzero(counts);best=int(ids[np.lexsort((ids,median[ids],-counts[ids]))[0]]) if len(ids) else -1
    return dict(squared_error=errors,inliers=inliers,counts=counts,median_error=median,best=best)
```
