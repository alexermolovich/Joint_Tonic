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

def functional_damped_step(position, velocity, force, mass, damping, dt):
    q=_float_array(position,2,1e4);v=_float_array(velocity,2,1e4);f=_float_array(force,2,1e4)
    m=_float_array(mass,1);c=_float_array(damping,1);h=_real(dt,1e-6,.1)
    if q.shape!=v.shape or q.shape!=f.shape or q.shape[0]>4096 or not 1<=q.shape[1]<=64 or q.size>100000:
        raise ValueError('Invalid state shape')
    if m.shape!=(q.shape[1],) or c.shape!=m.shape or np.any(m<1e-3) or np.any(m>1e3) or np.any(c<0) or np.any(c>1e3):
        raise ValueError('Invalid physical parameters')
    acceleration=(f-c*v)/m
    next_velocity=v+h*acceleration
    next_position=q+h*next_velocity
    return dict(position=next_position,velocity=next_velocity)
