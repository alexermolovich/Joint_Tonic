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

def se3_maps(tangent,transform):
    xi=_array(tangent,1);t=_array(transform,2);limit=np.pi-1e-4
    if xi.shape!=(6,) or t.shape!=(4,4) or np.linalg.norm(xi[:3])>1e6 or np.linalg.norm(xi[3:])>limit:raise ValueError("SE3 map input")
    _transform(t);r=t[:3,:3];sine_vector=.5*np.array([r[2,1]-r[1,2],r[0,2]-r[2,0],r[1,0]-r[0,1]]);sine=float(np.linalg.norm(sine_vector));cosine=float(np.clip((np.trace(r)-1)/2,-1,1));angle=float(np.arctan2(sine,cosine))
    if angle>limit:raise ValueError("principal rotation branch")
    scale=1+angle*angle/6+7*angle**4/360 if angle<1e-4 else angle/sine;phi=scale*sine_vector
    log=np.r_[np.linalg.solve(_left_jacobian(phi),t[:3,3]),phi];out=np.eye(4);out[:3,:3]=_so3(xi[3:]);out[:3,3]=_left_jacobian(xi[3:])@xi[:3]
    return dict(exponential=out,logarithm=log)
