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

def _policy_inputs(new_logp,old_logp,advantages,valid,epsilon):
    new=_array(new_logp,2);old=_array(old_logp,2);a=_array(advantages,2);m=_array(valid,2,"bool");eps=_scalar(epsilon,0,1)
    if not 1<=new.shape[0]<=64 or not 1<=new.shape[1]<=1024 or old.shape!=new.shape or a.shape!=new.shape or m.shape!=new.shape or (np.abs(new)>100).any() or (np.abs(old)>100).any() or (np.abs(new-old)>40).any():raise ValueError("policy batch contract")
    return new-old,a,m,eps

def clipped_surrogate(new_logp,old_logp,advantages,valid,epsilon):
    delta,a,m,eps=_policy_inputs(new_logp,old_logp,advantages,valid,epsilon);ratio=np.exp(delta)
    terms=np.where(m,np.minimum(ratio*a,np.clip(ratio,1-eps,1+eps)*a),0.);count=int(m.sum());objective=float(terms.sum()/count) if count else 0.
    return {'terms':terms,'objective':objective,'loss':-objective}
