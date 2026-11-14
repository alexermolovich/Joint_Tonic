import math

import numpy as np

def _integer_array(x, ndim):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('int64') or x.ndim!=ndim:
        raise ValueError('Expected int64 array')
    return x

def _integer(x, lo, hi):
    if type(x) is not int or not lo<=x<=hi:
        raise ValueError('Invalid integer scalar')
    return x

def simulation_throughput(start_ns, end_ns, environment_steps, learner_updates, warmup):
    s=_integer_array(start_ns,1);e=_integer_array(end_ns,1);n=_integer_array(environment_steps,1);u=_integer_array(learner_updates,1)
    if len(s)>100000 or any(v.shape!=s.shape for v in (e,n,u)) or np.any(s<0) or np.any(e<0) or np.any(e<=s):
        raise ValueError('Invalid interval arrays')
    if np.any(e[:-1]>s[1:]) or any(np.any(v<0) or np.any(v>1000000000) for v in (n,u)):
        raise ValueError('Invalid chronology or counts')
    _integer(warmup,0,len(s))
    duration=sum(int(b)-int(a) for a,b in zip(s[warmup:],e[warmup:]));steps=sum(map(int,n[warmup:]));updates=sum(map(int,u[warmup:]))
    return dict(duration_ns=duration,environment_steps=steps,learner_updates=updates,steps_per_second=steps*1e9/duration if duration else float('nan'),updates_per_second=updates*1e9/duration if duration else float('nan'))
