import math

import numpy as np

def _float_array(x, ndim, bound=1e6):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:
        raise ValueError('Expected floating array with documented dimensions')
    y=x.astype(np.float64)
    if not np.all(np.isfinite(y)) or np.any(np.abs(y)>bound):
        raise ValueError('Invalid floating values')
    return y

def _boolean_array(x, shape):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('bool') or x.shape!=shape:
        raise ValueError('Expected matching Boolean array')
    return x

def _integer(x, lo, hi):
    if type(x) is not int or not lo<=x<=hi:
        raise ValueError('Invalid integer scalar')
    return x

def aggregate_action_repeat(rewards, discounts, last, repeat):
    r=_float_array(rewards,1);d=_float_array(discounts,1)
    if not 1<=len(r)<=100000 or d.shape!=r.shape or np.any(d<0) or np.any(d>1):
        raise ValueError('Invalid transition arrays')
    last=_boolean_array(last,r.shape);_integer(repeat,1,len(r))
    total=0.;weight=1.;count=0
    for i in range(repeat):
        total+=weight*float(r[i]);weight*=float(d[i]);count=i+1
        if last[i]:break
    return dict(reward=float(total),discount=float(weight),steps=count,last=bool(last[count-1]))
