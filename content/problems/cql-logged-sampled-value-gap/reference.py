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

def action_value_gap(logged_values,sampled_values,logged_valid,sampled_valid,threshold):
    l=_array(logged_values,2);s=_array(sampled_values,2);lm=_array(logged_valid,2,"bool");sm=_array(sampled_valid,2,"bool");t=_scalar(threshold,0,1e6)
    if not 1<=len(l)<=128 or len(s)!=len(l) or not 1<=l.shape[1]<=256 or not 1<=s.shape[1]<=256 or lm.shape!=l.shape or sm.shape!=s.shape:raise ValueError("gap contract")
    lc=lm.sum(axis=1,dtype=np.int64);sc=sm.sum(axis=1,dtype=np.int64);lv=np.full(len(l),np.nan);sv=lv.copy()
    np.divide(np.where(lm,l,0).sum(axis=1),lc,out=lv,where=lc>0);np.divide(np.where(sm,s,0).sum(axis=1),sc,out=sv,where=sc>0);gap=sv-lv
    return {'logged_mean':lv,'sample_mean':sv,'gap':gap,'counts':np.stack([lc,sc],axis=1),'flagged':(lc>0)&(sc>0)&(gap>t)}
