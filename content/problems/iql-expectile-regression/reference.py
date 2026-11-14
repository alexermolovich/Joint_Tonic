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

def expectile_loss(q_targets,values,valid,tau):
    q=_array(q_targets,2);v=_array(values,2);m=_array(valid,2,"bool");t=_scalar(tau,.001,.999)
    if not 1<=len(q)<=64 or not 1<=q.shape[1]<=1024 or v.shape!=q.shape or m.shape!=q.shape:raise ValueError("expectile contract")
    u=q-v;w=np.where(u>=0,t,1-t);terms=np.where(m,w*u*u,0.);n=int(m.sum());grad=np.where(m,-2*w*u/n,0.) if n else np.zeros_like(q)
    return {'loss':float(terms.sum()/n) if n else 0.,'per_element':terms,'value_gradient':grad}
