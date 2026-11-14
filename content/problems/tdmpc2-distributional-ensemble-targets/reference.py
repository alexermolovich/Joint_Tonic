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

def distributional_targets(rewards,next_values,critic_indices,terminated,bins,gamma):
    r=_array(rewards,1);q=_array(next_values,2);idx=_array(critic_indices,2,"int");done=_array(terminated,1,"bool");bins=_array(bins,1);g=_scalar(gamma,0,1);b=len(r);k=len(bins)
    if b>1024 or q.shape[0]!=b or not 2<=q.shape[1]<=16 or idx.shape!=(b,2) or done.shape!=(b,) or not 2<=k<=255 or (np.diff(bins)<=0).any() or (np.abs(bins)>20).any() or (idx<0).any() or (idx>=q.shape[1]).any() or (idx[:,0]==idx[:,1]).any():raise ValueError("ensemble target contract")
    bootstrap=np.min(q[np.arange(b)[:,None],idx],axis=1);target=r+g*(~done)*bootstrap
    def encode(x):
        y=np.clip(np.sign(x)*np.log1p(np.abs(x)),bins[0],bins[-1]);hi=np.clip(np.searchsorted(bins,y,side='right'),1,k-1);lo=hi-1;upper=(y-bins[lo])/(bins[hi]-bins[lo]);out=np.zeros((b,k));rows=np.arange(b);out[rows,lo]=1-upper;out[rows,hi]=upper;return out
    return {'bootstrap':bootstrap,'td_target':target,'reward_targets':encode(r),'value_targets':encode(target)}
