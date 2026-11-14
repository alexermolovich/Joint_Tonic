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

def relative_odometry(poses, times, edges):
    t=_transform(_array(poses,3));time=_array(times,1);edge=_array(edges,2,"i");n=len(t);e=len(edge)
    if not 1<=n<=8192 or time.shape!=(n,) or np.any(np.diff(time)<1e-6) or edge.shape!=(e,2) or e>32768 or np.any(edge<0) or np.any(edge>=n) or np.any(edge[:,0]>=edge[:,1]):raise ValueError("odometry edge contract")
    i,j=edge.T;ri=t[i,:3,:3].swapaxes(1,2);out=np.broadcast_to(np.eye(4),(e,4,4)).copy();out[:,:3,:3]=ri@t[j,:3,:3];out[:,:3,3]=np.einsum('nij,nj->ni',ri,t[j,:3,3]-t[i,:3,3]);dt=time[j]-time[i]
    return dict(transforms=out,durations=dt,speeds=np.linalg.norm(out[:,:3,3],axis=1)/dt)
