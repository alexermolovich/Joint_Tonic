# Solution

Compose endpoint lidar poses, invert the first rigidly, then compare with the supplied measurement. Rotation logarithm uses stable small-angle and near-pi conventions. Fixed-size inputs give constant time/storage.

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

def _skew(v):
    x,y,z=v
    return np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])

def _exp(phi):
    theta=float(np.linalg.norm(phi));s=theta*theta;k=_skew(phi)
    if theta<1e-4:a=1-s/6+s*s/120;b=.5-s/24+s*s/720
    else:a=np.sin(theta)/theta;b=(1-np.cos(theta))/s
    return np.eye(3)+a*k+b*(k@k)

def _log(r):
    v=np.array([r[2,1]-r[1,2],r[0,2]-r[2,0],r[1,0]-r[0,1]])/2;s=float(np.linalg.norm(v));c=float(np.clip((np.trace(r)-1)/2,-1,1));angle=float(np.arctan2(s,c))
    if angle>np.pi-1e-4:raise ValueError("rotation error outside principal branch contract")
    return v*(1+angle*angle/6+7*angle**4/360) if angle<1e-4 else v*(angle/s)

def imu_lidar_residual(world_from_imu, imu_from_lidar, lidar_relative, std):
    poses=_transform(_array(world_from_imu,3));ext=_transform(_array(imu_from_lidar,2));measured=_transform(_array(lidar_relative,2));s=_array(std,1)
    if poses.shape!=(2,4,4) or ext.shape!=(4,4) or measured.shape!=(4,4) or s.shape!=(6,) or np.any((s<1e-6)|(s>1000)):raise ValueError("lidar pose constraint")
    lidar=poses@ext;pred=np.eye(4);pred[:3,:3]=lidar[0,:3,:3].T@lidar[1,:3,:3];pred[:3,3]=lidar[0,:3,:3].T@(lidar[1,:3,3]-lidar[0,:3,3]);error_rotation=measured[:3,:3].T@pred[:3,:3];translation=measured[:3,:3].T@(pred[:3,3]-measured[:3,3]);rotation=_log(error_rotation);white=np.concatenate([translation,rotation])/s
    return dict(predicted=pred,translation=translation,rotation=rotation,whitened=white,cost=float(.5*(white@white)))
```
