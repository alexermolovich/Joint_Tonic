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

def deskew_points(points,world_from_capture,world_from_reference):
    p=_array(points,2);capture=_array(world_from_capture,3);ref=_array(world_from_reference,2)
    if p.shape[1]!=3 or len(p)>8192 or capture.shape!=(len(p),4,4) or ref.shape!=(4,4):raise ValueError("deskew shape")
    _transform(capture);_transform(ref);world=np.einsum('nij,nj->ni',capture[:,:3,:3],p)+capture[:,:3,3]
    return (world-ref[:3,3])@ref[:3,:3]
