# Solution

Use a dictionary keyed by voxel coordinate, updating a winner only for a strictly smaller center distance. Sort the occupied keys at the end. O((M+N)+V log V) expected time, O(M+N) storage; no pairwise point-distance matrix.

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

def update_local_map(existing, scan, world_from_lidar, center, half_extent, voxel_size):
    old=_array(existing,2);new=_array(scan,2);t=_transform(_array(world_from_lidar,2));mid=_array(center,1);extent=_array(half_extent,1);size=_scalar(voxel_size,1e-3,1000);m=len(old);n=len(new)
    if m>16384 or n>16384 or old.shape!=(m,3) or new.shape!=(n,3) or t.shape!=(4,4) or mid.shape!=(3,) or extent.shape!=(3,) or np.any(np.abs(old)>1e4) or np.any(np.abs(new)>1e4) or np.any(np.abs(t[:3,3])>1e4) or np.any(np.abs(mid)>1e4) or np.any((extent<1e-3)|(extent>1e4)):raise ValueError("local map contract")
    candidates=np.concatenate([old,new@t[:3,:3].T+t[:3,3]],axis=0);inside=np.all(np.abs(candidates-mid)<=extent,axis=1);best={}
    for i in np.flatnonzero(inside):
        point=candidates[i];key=tuple(np.floor(point/size).astype(np.int64));voxel_center=(np.array(key,dtype=float)+.5)*size;distance=float(np.sum((point-voxel_center)**2));previous=best.get(key)
        if previous is None or distance<previous[0]:best[key]=(distance,int(i))
    keys=sorted(best);indices=np.array([best[key][1] for key in keys],np.int64);removed=np.ones(m,bool);removed[indices[indices<m]]=False
    return dict(points=candidates[indices].copy(),voxel_keys=np.array(keys,np.int64).reshape(-1,3),source_indices=indices,removed_existing=removed)
```
