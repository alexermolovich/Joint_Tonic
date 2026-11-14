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

def update_terrain_levels(levels,positions,origins,commands,reset,terrain_length,episode_seconds,num_levels,restart_draws):
    level=_array(levels,1,"int");p=_array(positions,2);o=_array(origins,2);c=_array(commands,2);mask=_array(reset,1,"bool");draw=_array(restart_draws,1);length=_scalar(terrain_length,1e-3,1e4);seconds=_scalar(episode_seconds,1e-3,1000);b=len(level)
    if type(num_levels) is not int:raise ValueError("level count")
    count=_scalar(num_levels,1,1024,True)
    if b>16384 or any(x.shape!=(b,2) for x in [p,o,c]) or mask.shape!=(b,) or draw.shape!=(b,) or ((level<0)|(level>=count)).any() or any((np.abs(x)>1e4).any() for x in [p,o]) or (np.abs(c)>100).any() or ((draw<0)|(draw>=1)).any():raise ValueError("terrain curriculum contract")
    distance=np.linalg.norm(p-o,axis=1);up=mask&(distance>length/2);down=mask&(distance<np.linalg.norm(c,axis=1)*seconds/2)&~up;candidate=level+up.astype(np.int64)-down.astype(np.int64);reassigned=mask&(candidate>=count);next_level=np.where(reassigned,np.floor(draw*count).astype(np.int64),np.maximum(candidate,0))
    return dict(levels=next_level,move_up=up,move_down=down,reassigned=reassigned,distance=distance)
