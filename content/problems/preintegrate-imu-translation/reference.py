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

def preintegrate_translation(accelerations,accelerometer_bias,relative_rotations,durations):
    a=_array(accelerations,2);b=_array(accelerometer_bias,1);r=_array(relative_rotations,3);dt=_array(durations,1);n=len(a)
    if a.shape[1]!=3 or n>4096 or b.shape!=(3,) or r.shape!=(n,3,3) or dt.shape!=(n,) or np.any(np.abs(a)>100) or np.any(np.abs(b)>100) or np.any((dt<1e-6)|(dt>1)) or dt.sum()>100:raise ValueError("translation integration contract")
    _rotation(r);forces=np.einsum('nij,nj->ni',r,a-b);v=np.zeros((n+1,3));p=np.zeros((n+1,3))
    for k in range(n):p[k+1]=p[k]+v[k]*dt[k]+.5*forces[k]*dt[k]**2;v[k+1]=v[k]+forces[k]*dt[k]
    return dict(velocity=v,position=p,elapsed=np.r_[0.,np.cumsum(dt)])
