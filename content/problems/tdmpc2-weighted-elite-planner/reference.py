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

def update_elite_distribution(actions,scores,valid,num_elites,inverse_temperature,min_std,max_std):
    a=_array(actions,3);s=_array(scores,1);m=_array(valid,1,"bool");k,h,d=a.shape
    if type(num_elites) is not int:raise ValueError("elite count type")
    n=_scalar(num_elites,1,k,True);beta=_scalar(inverse_temperature,0,100);low=_scalar(min_std,0,2);high=_scalar(max_std,low,2)
    if not 1<=k<=1024 or not 1<=h<=64 or not 1<=d<=32 or s.shape!=(k,) or m.shape!=(k,) or (np.abs(a)>1).any() or m.sum()<n:raise ValueError("elite candidate contract")
    ids=np.flatnonzero(m);chosen=ids[np.lexsort((ids,-s[ids]))[:n]];weights=np.exp(beta*(s[chosen]-s[chosen].max()));weights/=weights.sum();elite=a[chosen];mean=np.sum(weights[:,None,None]*elite,axis=0);variance=np.sum(weights[:,None,None]*(elite-mean)**2,axis=0);std=np.clip(np.sqrt(variance),low,high)
    return {'elite_indices':chosen,'weights':weights,'mean':mean,'std':std}
