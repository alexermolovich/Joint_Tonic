import math

import numpy as np

def _float_array(x, ndim, bound=1e6):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:
        raise ValueError('Expected floating array with documented dimensions')
    y=x.astype(np.float64)
    if not np.all(np.isfinite(y)) or np.any(np.abs(y)>bound):
        raise ValueError('Invalid floating values')
    return y

def _real(x, lo, hi):
    if type(x) not in (int,float) or not lo<=x<=hi or not math.isfinite(x):
        raise ValueError('Invalid real scalar')
    return float(x)

def tolerance_reward(values, lower, upper, margin, value_at_margin):
    x=_float_array(values,1)
    if len(x)>1000000:raise ValueError('Too many values')
    lo=_real(lower,-1e6,1e6);hi=_real(upper,-1e6,1e6)
    m=_real(margin,0,1e6);v=_real(value_at_margin,1e-6,1-1e-6)
    if lo>hi:raise ValueError('Reversed interval')
    distance=np.maximum(np.maximum(lo-x,x-hi),0)
    if m==0:return (distance==0).astype(np.float64)
    with np.errstate(over='ignore',under='ignore'):
        ratio=np.minimum(distance/m,1e6)
        return np.exp(math.log(v)*ratio*ratio)
