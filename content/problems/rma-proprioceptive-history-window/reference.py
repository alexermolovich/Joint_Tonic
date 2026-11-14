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

def window_history(observations,actions,episode_ids,query_indices,history_length):
    o=_array(observations,2);a=_array(actions,2);ep=_array(episode_ids,1,"int");q=_array(query_indices,1,"int")
    if type(history_length) is not int:raise ValueError("built-in history length required")
    h=_scalar(history_length,1,64,True);n=len(o)
    if not 1<=n<=4096 or not 1<=o.shape[1]<=32 or a.shape[0]!=n or not 1<=a.shape[1]<=32 or ep.shape!=(n,) or len(q)>128 or (ep<0).any() or (np.diff(ep)<0).any() or (q<0).any() or (q>=n).any() or (np.abs(o)>100).any() or (np.abs(a)>100).any():raise ValueError("history contract")
    rows=q[:,None]-h+np.arange(h);safe=np.maximum(rows,0);valid=(rows>=0)&(ep[safe]==ep[q,None]);source=np.where(valid,rows,-1).astype(np.int64);features=np.concatenate([o,a],axis=1)
    return {'history':np.where(valid[...,None],features[safe],0.),'valid':valid,'source_indices':source}
