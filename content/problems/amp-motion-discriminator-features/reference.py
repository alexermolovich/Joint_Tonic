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

def motion_features(root_positions,root_yaw,root_velocity,root_angular_velocity,joint_rotations,joint_velocities,endpoints):
    p=_array(root_positions,3);yaw=_array(root_yaw,2);v=_array(root_velocity,3);w=_array(root_angular_velocity,3);rot=_array(joint_rotations,5);jv=_array(joint_velocities,4);ep=_array(endpoints,4)
    if not 1<=len(p)<=64 or p.shape[1:]!=(2,3) or yaw.shape!=(len(p),2) or v.shape!=p.shape or w.shape!=p.shape or rot.shape[:2]!=(len(p),2) or not 1<=rot.shape[2]<=32 or rot.shape[3:]!=(3,3) or jv.shape!=rot.shape[:3]+(3,) or ep.shape[:2]!=(len(p),2) or not 1<=ep.shape[2]<=8 or ep.shape[3]!=3 or (np.abs(yaw)>np.pi).any():raise ValueError("motion feature shape")
    if not np.allclose(np.swapaxes(rot,-1,-2)@rot,np.eye(3),atol=1e-6,rtol=0) or not np.allclose(np.linalg.det(rot),1,atol=1e-6,rtol=0):raise ValueError("proper joint rotations required")
    c=np.cos(yaw);s=np.sin(yaw);r=np.zeros(p.shape[:2]+(3,3));r[...,0,0]=c;r[...,0,2]=s;r[...,1,1]=1;r[...,2,0]=-s;r[...,2,2]=c
    lv=np.einsum('btij,bti->btj',r,v);lw=np.einsum('btij,bti->btj',r,w);le=np.einsum('btij,btei->btej',r,ep-p[:,:,None,:]);b=len(p)
    rc=np.swapaxes(rot[...,:,:2],-1,-2).reshape(b,2,-1)
    phi=np.concatenate([lv,lw,rc,jv.reshape(b,2,-1),le.reshape(b,2,-1)],axis=-1)
    return phi.reshape(b,-1).copy()
