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

def terrain_clearance_report(foot_positions,terrain_height,swing,observed,terrain_ids,minimum_clearance,num_terrains):
    p=_array(foot_positions,4);h=_array(terrain_height,3);s=_array(swing,3,"bool");o=_array(observed,3,"bool");ids=_array(terrain_ids,1,"int");threshold=_array(minimum_clearance,1);b,t,f,d=p.shape
    if type(num_terrains) is not int:raise ValueError("terrain count")
    k=_scalar(num_terrains,1,64,True)
    if b>128 or not 1<=t<=256 or not 1<=f<=4 or d!=3 or any(x.shape!=(b,t,f) for x in [h,s,o]) or ids.shape!=(b,) or ((ids<0)|(ids>=k)).any() or threshold.shape!=(k,) or ((threshold<0)|(threshold>1)).any() or (np.abs(p)>1e4).any() or (np.abs(h)>1e4).any():raise ValueError("clearance contract")
    eligible=s&o;clearance=np.where(eligible,p[:,:,:,2]-h,np.nan);counts=np.zeros(k,np.int64);means=np.full(k,np.nan);minimum=np.full(k,np.nan);rates=np.full(k,np.nan)
    for terrain in range(k):
        mask=eligible&(ids[:,None,None]==terrain);values=clearance[mask];counts[terrain]=len(values)
        if len(values):means[terrain]=values.mean();minimum[terrain]=values.min();rates[terrain]=np.mean(values<threshold[terrain])
    return dict(clearance=clearance,counts=counts,mean_clearance=means,min_clearance=minimum,violation_rate=rates)
