# Solution

Transform each point into each camera, project valid depths, and keep depth separate. Time and storage O(CN).

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def project_bev(points, ego_to_camera, intrinsics):
    p=_array(points,2);t=_array(ego_to_camera,3);k=_array(intrinsics,3)
    if p.shape[1:]!=(3,) or len(p)>4096 or t.shape[1:]!=(4,4) or not 1<=len(t)<=16 or k.shape!=(len(t),3,3):raise ValueError("Shape")
    r=t[:,:3,:3]
    if not np.all(t[:,3]==[0,0,0,1]) or not np.allclose(r.transpose(0,2,1)@r,np.eye(3),rtol=0,atol=1e-8) or not np.all(np.abs(np.linalg.det(r)-1)<=1e-8):raise ValueError("Rigid transforms")
    if not np.all(k[:,[0,1,2,2,2],[1,0,0,1,2]]==[0,0,0,0,1]) or np.any(k[:,[0,1],[0,1]]<1e-6):raise ValueError("Intrinsics")
    cam=np.einsum('cij,nj->cni',r,p)+t[:,:3,3,None].transpose(0,2,1)
    z=cam[:,:,2].copy();uv=np.zeros((len(t),len(p),2));valid=z>1e-6
    for j in range(2):
        np.divide(cam[:,:,j],z,out=uv[:,:,j],where=valid)
        uv[:,:,j]=np.where(valid,uv[:,:,j]*k[:,j,j,None]+k[:,j,2,None],0.)
    return uv,z
```
