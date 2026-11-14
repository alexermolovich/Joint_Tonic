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

def route_dual_system(context,state,embodiment_ids,state_projectors,context_time,observation_time,max_context_age):
    h=_array(context,2);s=_array(state,2);ids=_array(embodiment_ids,1,"int");p=_array(state_projectors,3);ct=_array(context_time,1);ot=_array(observation_time,1);limit=_scalar(max_context_age);b,c=h.shape
    if not 1<=b<=64 or not 1<=c<=64 or s.shape[0]!=b or not 1<=s.shape[1]<=64 or not 1<=len(p)<=16 or p.shape[1]!=s.shape[1] or not 1<=p.shape[2]<=64 or ids.shape!=(b,) or ct.shape!=(b,) or ot.shape!=(b,) or (ids<0).any() or (ids>=len(p)).any() or (ct<0).any() or (ot<0).any():raise ValueError("dual-system contract")
    projected=np.einsum('bs,bse->be',s,p[ids]);age=ot-ct
    return {'conditioning':np.concatenate([h,projected],axis=1),'head_ids':ids.copy(),'ready':(age>=0)&(age<=limit),'context_age':age}
