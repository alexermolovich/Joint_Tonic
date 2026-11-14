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

def tanh_action_logprob(pre_tanh,base_logprob,action_scale):
    u=_array(pre_tanh,2);p=_array(base_logprob,1);s=_array(action_scale,1)
    if not 1<=len(u)<=128 or not 1<=u.shape[1]<=64 or p.shape!=(len(u),) or s.shape!=(u.shape[1],) or (np.abs(u)>100).any() or (s<1e-6).any() or (s>1000).any():raise ValueError("squash contract")
    log_jac=2*(np.log(2.)-u-np.logaddexp(0.,-2*u))
    return {'actions':s*np.tanh(u),'log_prob':p-(np.log(s)+log_jac).sum(axis=1)}
