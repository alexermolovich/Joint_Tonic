import numpy as np

def _int(v,lo=0,hi=2**63-1):
    if type(v) is not int or not lo<=v<=hi:raise ValueError('integer')
    return v

def _numeric(v,rank):
    if not isinstance(v,np.ndarray) or v.dtype not in (np.dtype('float32'),np.dtype('float64')) or v.ndim!=rank or v.size>10**6 or not np.isfinite(v).all() or (v.size and np.max(np.abs(v))>1e6):raise ValueError('numeric array')
    return v.astype(np.float64)

def _ints(v,rank=1):
    if not isinstance(v,np.ndarray) or v.dtype!=np.int64 or v.ndim!=rank:raise ValueError('integer array')
    return v

def action_segment_report(times_ns, actions, observed, max_command, deadband, min_samples, min_duration_ns):
    t=_ints(times_ns);limit=_numeric(max_command,1)
    if not isinstance(actions,np.ndarray) or actions.dtype not in (np.dtype('float32'),np.dtype('float64')) or actions.ndim!=2 or actions.size>10**6:raise ValueError('actions')
    a=actions.astype(np.float64);T,D=a.shape
    if T>100000 or not 1<=D<=32 or t.shape!=(T,) or limit.shape!=(D,) or np.any(limit<=0) or np.any(t<0) or np.any(t[1:]<=t[:-1]):raise ValueError('shape/time/limit')
    if not isinstance(observed,np.ndarray) or observed.dtype!=np.bool_ or observed.shape!=(T,):raise ValueError('observed')
    if type(deadband) not in (int,float) or not 0<=deadband<=float(limit.min()) or not np.isfinite(deadband):raise ValueError('deadband')
    _int(min_samples,1,100000);_int(min_duration_ns)
    magnitude=np.abs(a);corrupt=(~observed)|(~np.isfinite(a).all(axis=1))|(magnitude>limit).any(axis=1)
    candidate=(~corrupt)&(magnitude<=deadband).all(axis=1);paused=np.zeros(T,dtype=bool);segments=[];start=None
    for i in range(T+1):
        if i<T and candidate[i]:
            if start is None:start=i
        elif start is not None:
            duration=int(t[i-1])-int(t[start])
            if i-start>=min_samples and duration>=min_duration_ns:paused[start:i]=True;segments.append((start,i,duration))
            start=None
    return dict(corrupt=corrupt,paused=paused,segments=segments)
