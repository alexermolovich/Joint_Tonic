import numpy as np

def _array(value, ndim=None, kind="real"):
    try: a=np.asarray(value)
    except (ValueError,TypeError,OverflowError) as e: raise ValueError("invalid array") from e
    if ndim is not None and a.ndim!=ndim: raise ValueError("invalid rank")
    if a.size>1000000: raise ValueError("array too large")
    if kind=="bool":
        if a.dtype.kind!='b': raise ValueError("boolean array required")
        return a.copy()
    if kind=="int":
        if a.dtype.kind not in 'iu': raise ValueError("integer array required")
    elif a.dtype.kind not in 'iuf': raise ValueError("real numeric array required")
    if not np.isfinite(a).all() or (np.abs(a.astype(np.float64))>1e6).any(): raise ValueError("invalid numeric values")
    return a.astype(np.int64 if kind=="int" else np.float64)

def _scalar(x,low=0,high=1e6,integer=False):
    if isinstance(x,(bool,np.bool_)) or not isinstance(x,(int,float,np.integer,np.floating)): raise ValueError("numeric scalar required")
    if integer and not isinstance(x,(int,np.integer)): raise ValueError("integer scalar required")
    if not low<=x<=high or not np.isfinite(x): raise ValueError("scalar outside bounds")
    return int(x) if integer else float(x)

def gait_metrics(linear_velocity,angular_velocity,command,projected_gravity,valid,linear_scale,yaw_scale):
    v=_array(linear_velocity,3);w=_array(angular_velocity,3);c=_array(command,3);g=_array(projected_gravity,3);m=_array(valid,2,"bool");sv=_scalar(linear_scale,1e-6,1000);sw=_scalar(yaw_scale,1e-6,1000);b,t,d=v.shape
    if b>128 or not 1<=t<=256 or d!=3 or any(x.shape!=v.shape for x in [w,c,g]) or m.shape!=(b,t) or any((np.abs(x)>100).any() for x in [v,w,c]) or not np.allclose(np.linalg.norm(g,axis=2),1,atol=1e-7,rtol=0):raise ValueError("gait metric contract")
    ev=np.sum((v[:,:,:2]-c[:,:,:2])**2,axis=2);ew=(w[:,:,2]-c[:,:,2])**2;terms=np.stack([np.exp(-ev/sv),np.exp(-ew/sw),v[:,:,2]**2,np.sum(w[:,:,:2]**2,axis=2),np.sum(g[:,:,:2]**2,axis=2)],axis=2);terms[~m]=0;count=m.sum(axis=1,dtype=np.int64);means=np.divide(terms.sum(axis=1),count[:,None],out=np.full((b,5),np.nan),where=count[:,None]>0)
    return dict(per_step=terms,counts=count,means=means)
