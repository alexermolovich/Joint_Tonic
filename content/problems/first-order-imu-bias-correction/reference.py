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

def _skew(v):
    x,y,z=v
    return np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])

def _so3(phi):
    theta=float(np.linalg.norm(phi));s=theta*theta;k=_skew(phi)
    if theta<1e-4:a=1-s/6+s*s/120;b=.5-s/24+s*s/720
    else:a=np.sin(theta)/theta;b=(1-np.cos(theta))/s
    return np.eye(3)+a*k+b*(k@k)

def _left_jacobian(phi):
    theta=float(np.linalg.norm(phi));s=theta*theta;k=_skew(phi)
    if theta<1e-4:b=.5-s/24+s*s/720;c=1/6-s/120+s*s/5040
    else:b=(1-np.cos(theta))/s;c=(theta-np.sin(theta))/(s*theta)
    return np.eye(3)+b*k+c*(k@k)

def correct_preintegration(delta_rotation,delta_velocity,delta_position,jacobians,gyro_delta,accel_delta):
    r=_array(delta_rotation,2);v=_array(delta_velocity,1);p=_array(delta_position,1);j=_array(jacobians,3);bg=_array(gyro_delta,1);ba=_array(accel_delta,1)
    if r.shape!=(3,3) or v.shape!=(3,) or p.shape!=(3,) or j.shape!=(5,3,3) or bg.shape!=(3,) or ba.shape!=(3,) or np.linalg.norm(bg)>.01 or np.linalg.norm(ba)>.01:raise ValueError("bias correction contract")
    _rotation(r);phi=j[0]@bg
    if np.linalg.norm(phi)>.1:raise ValueError("rotation correction too large")
    return dict(rotation=r@_so3(phi),velocity=v+j[1]@bg+j[2]@ba,position=p+j[3]@bg+j[4]@ba)
