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

def keyframe_residual(rotations,positions,velocities,gravity,duration,delta_rotation,delta_velocity,delta_position,imu_std,visual_residuals,visual_std):
    r=_array(rotations,3);p=_array(positions,2);v=_array(velocities,2);g=_array(gravity,1);t=_scalar(duration,1e-6,100);dr=_array(delta_rotation,2);dv=_array(delta_velocity,1);dp=_array(delta_position,1);std=_array(imu_std,1);visual=_array(visual_residuals,2);vs=_array(visual_std,2)
    if r.shape!=(2,3,3) or p.shape!=(2,3) or v.shape!=(2,3) or g.shape!=(3,) or np.any(np.abs(g)>100) or dr.shape!=(3,3) or dv.shape!=(3,) or dp.shape!=(3,) or std.shape!=(9,) or visual.shape[1]!=2 or len(visual)>16384 or vs.shape!=visual.shape or np.any((std<1e-6)|(std>1000)) or np.any((vs<1e-6)|(vs>1000)):raise ValueError("keyframe residual contract")
    _rotation(r);_rotation(dr);rr=_log(dr.T@r[0].T@r[1]);rv=r[0].T@(v[1]-v[0]-g*t)-dv;rp=r[0].T@(p[1]-p[0]-v[0]*t-.5*g*t*t)-dp;inertial=np.r_[rr,rv,rp];whitened=np.r_[inertial/std,(visual/vs).ravel()]
    return dict(inertial=inertial,whitened=whitened,cost=float(.5*(whitened@whitened)))
