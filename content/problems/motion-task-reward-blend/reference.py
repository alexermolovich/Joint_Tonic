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

def combine_motion_rewards(motion_reward,task_reward,valid,motion_weight,task_weight):
    a=_array(motion_reward,2);b=_array(task_reward,2);m=_array(valid,2,"bool");wa=_scalar(motion_weight,0,100);wb=_scalar(task_weight,0,100)
    if not 1<=len(a)<=128 or not 1<=a.shape[1]<=256 or b.shape!=a.shape or m.shape!=a.shape or ((a<0)|(a>1)).any() or ((b<0)|(b>1)).any():raise ValueError("reward blend contract")
    ca=np.where(m,wa*a,0.);cb=np.where(m,wb*b,0.);reward=ca+cb
    return {'motion_contribution':ca,'task_contribution':cb,'reward':reward,'mean_reward':float(reward[m].mean()) if m.any() else 0.}
