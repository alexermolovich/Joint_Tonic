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

def interaction_statistics(trial_duration,intervention_duration,reset_duration,task_success,reset_success,valid):
    t=_array(trial_duration,1);h=_array(intervention_duration,1);r=_array(reset_duration,1);s=_array(task_success,1,"bool");reset=_array(reset_success,1,"bool");m=_array(valid,1,"bool")
    if len(t)>16384 or any(x.shape!=t.shape for x in [h,r,s,reset,m]) or any((x<0).any() for x in [t,h,r]) or (h>t).any():raise ValueError("interaction accounting contract")
    n=int(m.sum());autonomous=m&(h==0);na=int(autonomous.sum());trial=float(t[m].sum());human=float(h[m].sum());reset_time=float(r[m].sum())
    return {'trials':n,'autonomous_trials':na,'robot_time':trial+reset_time,'human_time':human,'reset_time':reset_time,'human_fraction':human/trial if trial else float('nan'),'task_success_rate':float(s[m].mean()) if n else float('nan'),'reset_success_rate':float(reset[m].mean()) if n else float('nan'),'autonomous_success_rate':float(s[autonomous].mean()) if na else float('nan')}
