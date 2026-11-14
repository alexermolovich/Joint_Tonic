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

def teacher_belief_loss(student_actions,teacher_actions,reconstruction,privileged_target,action_valid,reconstruction_valid,action_scale,feature_scale,weights):
    a=_array(student_actions,3);teacher=_array(teacher_actions,3);z=_array(reconstruction,3);target=_array(privileged_target,3);m=_array(action_valid,2,"bool");n=_array(reconstruction_valid,3,"bool");s=_array(action_scale,1);u=_array(feature_scale,1);w=_array(weights,1);b,t,d=a.shape
    if b>64 or not 1<=t<=128 or not 1<=d<=32 or teacher.shape!=a.shape or z.shape[:2]!=(b,t) or not 1<=z.shape[2]<=64 or target.shape!=z.shape or m.shape!=(b,t) or n.shape!=z.shape or s.shape!=(d,) or u.shape!=(z.shape[2],) or w.shape!=(2,):raise ValueError("teacher belief shapes")
    if any((np.abs(x)>10).any() for x in [a,teacher]) or any((np.abs(x)>100).any() for x in [z,target]) or ((s<1e-3)|(s>10)).any() or ((u<1e-3)|(u>100)).any() or ((w<0)|(w>100)).any():raise ValueError("teacher belief ranges")
    na=d*int(m.sum());nz=int(n.sum());ra=np.where(m[:,:,None],a-teacher,0.);rz=np.where(n,z-target,0.);components=np.array([np.sum((ra/s)**2)/max(na,1),np.sum((rz/u)**2)/max(nz,1)])
    return dict(components=components,counts=np.array([na,nz],np.int64),loss=float(w@components),action_gradient=2*w[0]*ra/(max(na,1)*s*s),reconstruction_gradient=2*w[1]*rz/(max(nz,1)*u*u))
