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

def reset_failed_locomotion(contact_force,episode_steps,max_steps,state,initial_state,last_action,feet_air_time):
    force=_array(contact_force,3);ticks=_array(episode_steps,1,"int");x=_array(state,2);initial=_array(initial_state,2);action=_array(last_action,2);air=_array(feet_air_time,2);b,k,d=force.shape
    if type(max_steps) is not int:raise ValueError("maximum steps")
    limit=_scalar(max_steps,1,1000000,True)
    if b>4096 or k>16 or d!=3 or ticks.shape!=(b,) or (ticks<0).any() or not 1<=x.shape[1]<=64 or x.shape[0]!=b or initial.shape!=x.shape or not 1<=action.shape[1]<=32 or action.shape[0]!=b or not 1<=air.shape[1]<=8 or air.shape[0]!=b or any((np.abs(q)>1e4).any() for q in [force,x,initial]) or (np.abs(action)>1).any() or ((air<0)|(air>100)).any():raise ValueError("locomotion reset contract")
    failure=(np.linalg.norm(force,axis=2)>1).any(axis=1);timeout=ticks>limit;reset=failure|timeout
    return dict(failure=failure,timeout=timeout,reset=reset,state=np.where(reset[:,None],initial,x),last_action=np.where(reset[:,None],0,action),feet_air_time=np.where(reset[:,None],0,air),episode_steps=np.where(reset,0,ticks).astype(np.int64))
