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

def assemble_token_groups(groups,present):
    if type(groups)!=list or type(present)!=list or not 1<=len(groups)<=16 or len(present)!=len(groups):raise ValueError("group lists")
    xs=[_array(x,3) for x in groups];ps=[_array(p,2,"bool") for p in present];b,_,e=xs[0].shape
    if not 1<=b<=16 or not 1<=e<=64 or any(x.shape[0]!=b or x.shape[2]!=e or x.shape[1]>128 or p.shape!=x.shape[:2] for x,p in zip(xs,ps)):raise ValueError("group shape")
    lengths=[x.shape[1] for x in xs];n=sum(lengths)
    if n>512 or b*n*e>1000000:raise ValueError("group capacity")
    return {'tokens':np.concatenate([np.where(p[:,:,None],x,0.) for x,p in zip(xs,ps)],axis=1),'present':np.concatenate(ps,axis=1),'group_ids':np.repeat(np.arange(len(xs),dtype=np.int64),lengths),'offsets':np.r_[0,np.cumsum(lengths)].astype(np.int64)}
