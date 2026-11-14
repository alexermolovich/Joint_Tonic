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

def preintegration_covariance(rotation_vectors, specific_force, durations, noise_variance):
    phi=_array(rotation_vectors,2);f=_array(specific_force,2);dt=_array(durations,1);q=_array(noise_variance,2);n=len(phi)
    if n>1024 or phi.shape!=(n,3) or f.shape!=(n,3) or dt.shape!=(n,) or q.shape!=(n,6) or np.any(np.linalg.norm(phi,axis=1)>3) or np.any(np.abs(f)>100) or np.any((dt<1e-6)|(dt>1)) or dt.sum()>100 or np.any((q<0)|(q>100)):raise ValueError("preintegration noise contract")
    cov=np.zeros((n+1,9,9));r=np.eye(3)
    for k in range(n):
        h=dt[k];v=phi[k];theta=float(np.linalg.norm(v));square=theta*theta;cross=_skew(v)
        if theta<1e-4:a=.5-square/24+square*square/720;b=1/6-square/120+square*square/5040
        else:a=(1-np.cos(theta))/square;b=(theta-np.sin(theta))/(square*theta)
        jr=np.eye(3)-a*cross+b*(cross@cross);increment=_exp(v);coupling=-r@_skew(f[k]);transition=np.eye(9);transition[:3,:3]=increment.T;transition[3:6,:3]=coupling*h;transition[6:,:3]=.5*coupling*h*h;transition[6:,3:6]=np.eye(3)*h
        noise=np.zeros((9,6));noise[:3,:3]=jr*h;noise[3:6,3:]=r*h;noise[6:,3:]=.5*r*h*h
        p=transition@cov[k]@transition.T+(noise*q[k])@noise.T;cov[k+1]=(p+p.T)/2;r=r@increment
    return dict(covariance=cov,final_rotation=r)
