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

def schedule_learner(new_transitions,warmup,ratio_numerator,ratio_denominator,max_updates_per_tick,publish_every):
    new=_array(new_transitions,1,"int")
    bounds=[(warmup,0,1000000),(ratio_numerator,1,32),(ratio_denominator,1,32),(max_updates_per_tick,1,1000),(publish_every,1,1000)]
    if any(type(x) is not int or not low<=x<=high for x,low,high in bounds) or len(new)>4096 or ((new<0)|(new>10000)).any():raise ValueError("learner schedule contract")
    updates=np.zeros(len(new),np.int64);completed=updates.copy();backlog=updates.copy();published=updates.copy();publish=np.zeros(len(new),bool);data=done=previous_bucket=current_version=0
    for t,amount in enumerate(new):
        data+=int(amount);target=max(data-warmup,0)*ratio_numerator//ratio_denominator;updates[t]=min(max_updates_per_tick,target-done);done+=int(updates[t]);completed[t]=done;backlog[t]=target-done;bucket=done//publish_every;publish[t]=bucket>previous_bucket
        if publish[t]:current_version=done
        published[t]=current_version;previous_bucket=bucket
    return {'updates':updates,'completed':completed,'backlog':backlog,'published_version':published,'publish':publish}
