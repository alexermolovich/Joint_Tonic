# Solution

Validate the shared transform and each feature geometry, transform scan points once, then compute normal projections and perpendicular line distances. O(P+L) time and memory.

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

def _rotation(r):
    if r.shape[-2:]!=(3,3) or not np.allclose(r.swapaxes(-1,-2)@r,np.eye(3),atol=1e-9,rtol=0) or not np.allclose(np.linalg.det(r),1,atol=1e-9,rtol=0):raise ValueError("proper rotation required")
    return r

def _transform(t):
    if t.shape[-2:]!=(4,4) or not np.allclose(t[...,3,:],[0,0,0,1],atol=1e-9,rtol=0):raise ValueError("rigid transform required")
    _rotation(t[...,:3,:3]);return t

def scan_residuals(plane_points,plane_anchors,plane_normals,line_points,line_a,line_b,world_from_lidar):
    p=_array(plane_points,2);q=_array(plane_anchors,2);n=_array(plane_normals,2);lp=_array(line_points,2);a=_array(line_a,2);b=_array(line_b,2);t=_array(world_from_lidar,2)
    if p.shape[1]!=3 or lp.shape[1]!=3 or len(p)>8192 or len(lp)>8192 or q.shape!=p.shape or n.shape!=p.shape or a.shape!=lp.shape or b.shape!=lp.shape or t.shape!=(4,4):raise ValueError("scan feature shape")
    _transform(t);norm=np.linalg.norm(n,axis=1);direction=b-a;length=np.linalg.norm(direction,axis=1)
    if np.any(np.abs(norm-1)>1e-9) or np.any(length<1e-6):raise ValueError("degenerate feature geometry")
    worldp=p@t[:3,:3].T+t[:3,3];worldl=lp@t[:3,:3].T+t[:3,3]
    plane=np.sum((n/norm[:,None])*(worldp-q),axis=1);line=np.linalg.norm(np.cross(worldl-a,direction),axis=1)/length
    return dict(plane=plane,line=line)
```
