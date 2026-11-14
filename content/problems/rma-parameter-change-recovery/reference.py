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

def recovery_metrics(times,errors,valid,change_index,tolerance,hold_samples):
    t=_array(times,1);e=_array(errors,2);m=_array(valid,2,"bool");tau=_scalar(tolerance,0,1e6)
    if type(change_index) is not int or type(hold_samples) is not int:raise ValueError("built-in integer index required")
    if not 1<=len(t)<=4096 or not 1<=len(e)<=128 or e.shape[1]!=len(t) or m.shape!=e.shape or (t<0).any() or (np.diff(t)<=0).any() or (e<0).any():raise ValueError("recovery trace contract")
    c=_scalar(change_index,0,len(t)-1,True);h=_scalar(hold_samples,1,len(t),True);good=m&(e<=tau);prefix=np.concatenate([np.zeros((len(e),1),np.int64),np.cumsum(good,axis=1,dtype=np.int64)],axis=1);runs=(prefix[:,h:]-prefix[:,:-h])==h;runs[:,:min(c,runs.shape[1])]=False
    recovered=runs.any(axis=1);idx=np.where(recovered,np.argmax(runs,axis=1),-1).astype(np.int64);delay=np.full(len(e),np.nan);delay[recovered]=t[idx[recovered]]-t[c];counts=m[:,c:].sum(axis=1,dtype=np.int64);mean=np.full(len(e),np.nan);np.divide(np.where(m[:,c:],e[:,c:],0).sum(axis=1),counts,out=mean,where=counts>0)
    return {'recovered':recovered,'index':idx,'delay':delay,'post_change_mean':mean,'counts':counts}
