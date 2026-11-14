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

def multiview_critic_loss(predictions,targets,valid):
    p=_array(predictions,2);y=_array(targets,1);m=_array(valid,2,"bool")
    if not 1<=len(p)<=128 or not 1<=p.shape[1]<=64 or y.shape!=(len(p),) or m.shape!=p.shape:raise ValueError("critic view contract")
    count=m.sum(axis=1);observed=count>0;n=int(observed.sum());res=p-y[:,None];per=np.full(len(p),np.nan)
    np.divide(np.where(m,res*res,0.).sum(axis=1),count,out=per,where=observed)
    grad=np.where(m,2*res/(np.maximum(count,1)[:,None]*max(n,1)),0.)
    return {'loss':float(per[observed].mean()) if n else 0.,'per_state':per,'gradient':grad}
