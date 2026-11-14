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

def select_adaptation_latent(control_times,completion_times,observation_times,latents,max_observation_age):
    t=_array(control_times,1);c=_array(completion_times,1);o=_array(observation_times,1);z=_array(latents,2);limit=_scalar(max_observation_age,0,100)
    if len(t)>4096 or len(c)>4096 or o.shape!=c.shape or z.shape[0]!=len(c) or not 1<=z.shape[1]<=32 or any((a<0).any() for a in [t,c,o]) or (np.diff(c)<=0).any() or (o>c).any() or (np.abs(z)>100).any():raise ValueError("asynchronous latent contract")
    ids=np.searchsorted(c,t,side='right').astype(np.int64)-1;present=ids>=0;obs=np.full(len(t),np.nan);done=obs.copy();obs[present]=t[present]-o[ids[present]];done[present]=t[present]-c[ids[present]];used=present&(obs<=limit);context=np.zeros((len(t),z.shape[1]));context[used]=z[ids[used]]
    return {'indices':ids,'observation_age':obs,'completion_age':done,'usable':used,'context':context}
