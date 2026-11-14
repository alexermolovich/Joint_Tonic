import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def camera_rays(pixels, intrinsics, camera_to_world):
    p=_array(pixels,2);k=_array(intrinsics,2);t=_array(camera_to_world,2)
    if p.shape[1:]!=(2,) or p.shape[0]>4096 or k.shape!=(3,3) or t.shape!=(4,4):raise ValueError("Shape")
    if not np.array_equal(k[[0,1,2,2,2],[1,0,0,1,2]],[0,0,0,0,1]) or min(k[0,0],k[1,1])<1e-6:raise ValueError("Intrinsics")
    r=t[:3,:3]
    if not np.array_equal(t[3],[0,0,0,1]) or not np.allclose(r.T@r,np.eye(3),rtol=0,atol=1e-8) or abs(np.linalg.det(r)-1)>1e-8:raise ValueError("Rigid transform")
    d=np.column_stack(((p[:,0]-k[0,2])/k[0,0],(p[:,1]-k[1,2])/k[1,1],np.ones(len(p))))@r.T
    d/=np.linalg.norm(d,axis=1,keepdims=True)
    return np.broadcast_to(t[:3,3],(len(p),3)).copy(),d
