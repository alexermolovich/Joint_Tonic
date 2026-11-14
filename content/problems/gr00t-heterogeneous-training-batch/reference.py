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

def heterogeneous_batch(observations,actions,source_ids,embodiment_ids):
    x=_array(observations,2);src=_array(source_ids,1,"int");emb=_array(embodiment_ids,1,"int");b,e=x.shape
    if not 1<=b<=32 or not 1<=e<=128 or type(actions)!=list or len(actions)!=b or src.shape!=(b,) or emb.shape!=(b,) or (src<0).any() or (src>2).any():raise ValueError("source batch")
    arrays=[];h=d=0
    for i,a in enumerate(actions):
        if src[i]==1:
            if a is not None or emb[i]!=-1:raise ValueError("video must not supply robot actions")
            arrays.append(None)
        else:
            if a is None or not 0<=emb[i]<=15:raise ValueError("robot requires embodiment and actions")
            v=_array(a,2)
            if not 1<=v.shape[0]<=64 or not 1<=v.shape[1]<=32:raise ValueError("action bounds")
            arrays.append(v);h=max(h,v.shape[0]);d=max(d,v.shape[1])
    y=np.zeros((b,h,d));mask=np.zeros((b,h,d),bool)
    for i,a in enumerate(arrays):
        if a is not None:y[i,:len(a),:a.shape[1]]=a;mask[i,:len(a),:a.shape[1]]=True
    return {'observations':x.copy(),'actions':y,'action_mask':mask,'source_ids':src.copy(),'embodiment_ids':emb.copy()}
