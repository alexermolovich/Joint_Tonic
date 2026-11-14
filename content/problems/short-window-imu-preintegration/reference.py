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

def preintegrate_window(angular_velocity,specific_force,gyro_bias,accel_bias,durations):
    w=_array(angular_velocity,2);f=_array(specific_force,2);bg=_array(gyro_bias,1);ba=_array(accel_bias,1);dt=_array(durations,1);n=len(w)
    if w.shape!=(n,3) or f.shape!=(n,3) or bg.shape!=(3,) or ba.shape!=(3,) or dt.shape!=(n,) or n>4096 or any(np.any(np.abs(x)>100) for x in [w,f,bg,ba]) or np.any((dt<1e-6)|(dt>1)) or dt.sum()>100:raise ValueError("IMU window contract")
    r=np.empty((n+1,3,3));v=np.zeros((n+1,3));p=np.zeros((n+1,3));r[0]=np.eye(3)
    for k in range(n):
        force=r[k]@(f[k]-ba);p[k+1]=p[k]+v[k]*dt[k]+.5*force*dt[k]**2;v[k+1]=v[k]+force*dt[k];r[k+1]=r[k]@_exp((w[k]-bg)*dt[k])
    return dict(rotations=r,velocity=v,position=p,elapsed=np.r_[0.,np.cumsum(dt)])
