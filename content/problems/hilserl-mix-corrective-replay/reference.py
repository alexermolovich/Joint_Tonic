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

def mix_corrective_replay(executed_actions,intervention,priorities,batch_size,intervention_fraction):
    a=_array(executed_actions,2);human=_array(intervention,1,"bool");p=_array(priorities,1);n,d=a.shape
    if type(batch_size) is not int:raise ValueError("batch count type")
    b=_scalar(batch_size,0,4096,True);fraction=_scalar(intervention_fraction,0,1)
    if n>16384 or not 1<=d<=16 or human.shape!=(n,) or p.shape!=(n,) or (np.abs(a)>1).any() or ((p<0)|(p>=1)).any():raise ValueError("corrective replay contract")
    nh=int(np.floor(b*fraction+.5));counts=np.array([nh,b-nh],np.int64);chosen=[]
    for label,count in zip([True,False],counts):
        ids=np.flatnonzero(human==label)
        if len(ids)<count:raise ValueError("insufficient source records")
        chosen.append(ids[np.lexsort((ids,p[ids]))[:int(count)]])
    indices=np.concatenate(chosen);return {'indices':indices,'actions':a[indices].copy(),'intervention':human[indices].copy(),'counts':counts}
