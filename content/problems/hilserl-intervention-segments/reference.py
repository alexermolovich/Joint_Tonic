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

def label_interventions(policy_actions,human_actions,intervention,episode_ids):
    p=_array(policy_actions,2);h=_array(human_actions,2);human=_array(intervention,1,"bool");ep=_array(episode_ids,1,"int");n,a=p.shape
    if n>16384 or not 1<=a<=16 or h.shape!=p.shape or human.shape!=(n,) or ep.shape!=(n,) or (ep<0).any() or (np.diff(ep)<0).any() or (np.abs(p)>1).any() or (np.abs(h)>1).any():raise ValueError("intervention record contract")
    executed=np.where(human[:,None],h,p);ids=np.full(n,-1,np.int64);segments=[]
    for i in range(n):
        if human[i]:
            if i==0 or not human[i-1] or ep[i]!=ep[i-1]:segments.append([int(ep[i]),i,i+1])
            else:segments[-1][2]=i+1
            ids[i]=len(segments)-1
    return {'executed_actions':executed,'segment_id':ids,'segments':np.asarray(segments,dtype=np.int64).reshape(-1,3)}
