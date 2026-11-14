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

def score_latent_trajectories(rewards,terminated,terminal_values,gamma):
    r=_array(rewards,2);done=_array(terminated,2,"bool");v=_array(terminal_values,1);g=_scalar(gamma,0,1);k,h=r.shape
    if not 1<=k<=1024 or h>128 or done.shape!=r.shape or v.shape!=(k,):raise ValueError("trajectory score contract")
    alive=np.concatenate([np.ones((k,1),bool),np.cumprod(~done,axis=1,dtype=np.int64).astype(bool)],axis=1);powers=g**np.arange(h);contributions=r*alive[:,:h]*powers;tail=(g**h)*alive[:,-1]*v;scores=contributions.sum(axis=1)+tail
    return {'contributions':contributions,'tail':tail,'scores':scores,'best':int(np.argmax(scores))}
