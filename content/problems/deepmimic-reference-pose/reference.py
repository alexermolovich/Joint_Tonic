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

def interpolate_motion(times,positions,rotations,query_times):
    t=_array(times,1);p=_array(positions,2);q=_array(rotations,3);query=_array(query_times,1)
    if not 2<=len(t)<=1024 or p.shape!=(len(t),3) or q.shape[0]!=len(t) or not 1<=q.shape[1]<=32 or q.shape[2]!=4 or len(query)>256 or (t<0).any() or (query<0).any() or (np.diff(t)<=0).any():raise ValueError("clip contract")
    norms=np.linalg.norm(q,axis=-1)
    if (np.abs(norms-1)>1e-6).any():raise ValueError("unit quaternion required")
    q=q/norms[...,None];clamped=np.clip(query,t[0],t[-1]);idx=np.clip(np.searchsorted(t,clamped,side='right')-1,0,len(t)-2);u=(clamped-t[idx])/(t[idx+1]-t[idx])
    low=q[idx];high=q[idx+1].copy();dot=np.sum(low*high,axis=-1);high=np.where((dot<0)[...,None],-high,high);dot=np.clip(np.abs(dot),0,1);near=dot>0.9995
    a=np.broadcast_to(u[:,None],dot.shape);out=(1-a[...,None])*low+a[...,None]*high
    theta=np.arccos(dot[~near]);frac=a[~near]
    out[~near]=(np.sin((1-frac)*theta)/np.sin(theta))[:,None]*low[~near]+(np.sin(frac*theta)/np.sin(theta))[:,None]*high[~near]
    out/=np.linalg.norm(out,axis=-1,keepdims=True)
    return {'positions':(1-u[:,None])*p[idx]+u[:,None]*p[idx+1],'rotations':out,'interval':idx.astype(np.int64),'alpha':u}
