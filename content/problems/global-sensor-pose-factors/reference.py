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

def global_factors(world_from_body, body_from_sensor, gps, magnetic, world_field, height, std, valid):
    body=_transform(_array(world_from_body,3));ext=_transform(_array(body_from_sensor,2));g=_array(gps,2);mag=_array(magnetic,2);field=_array(world_field,1);h=_array(height,1);s=_array(std,2);mask=_array(valid,2,"b");n=len(body)
    if n>4096 or ext.shape!=(4,4) or g.shape!=(n,3) or mag.shape!=(n,3) or field.shape!=(3,) or h.shape!=(n,) or s.shape!=(n,7) or mask.shape!=(n,3) or np.any((s<1e-6)|(s>1000)):raise ValueError("sensor factor contract")
    mn=np.linalg.norm(mag,axis=1);fn=np.linalg.norm(field)
    if np.any(mn<=1e-9) or fn<=1e-9:raise ValueError("magnetic direction undefined")
    sensor=body@ext;raw=np.zeros((n,7));raw[:,:3]=g-sensor[:,:3,3];raw[:,3:6]=mag/mn[:,None]-np.einsum('nji,j->ni',sensor[:,:3,:3],field/fn);raw[:,6]=h-sensor[:,2,3]
    available=np.concatenate([np.repeat(mask[:,:1],3,axis=1),np.repeat(mask[:,1:2],3,axis=1),mask[:,2:3]],axis=1);raw[~available]=0;white=raw/s
    return dict(raw=raw,whitened=white,cost=float(.5*np.sum(white*white)))
