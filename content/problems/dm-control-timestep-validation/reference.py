import math

import numpy as np

def _float_array(x, ndim, bound=1e6):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:
        raise ValueError('Expected floating array with documented dimensions')
    y=x.astype(np.float64)
    if not np.all(np.isfinite(y)) or np.any(np.abs(y)>bound):
        raise ValueError('Invalid floating values')
    return y

def _integer(x, lo, hi):
    if type(x) is not int or not lo<=x<=hi:
        raise ValueError('Invalid integer scalar')
    return x

def _real(x, lo, hi):
    if type(x) not in (int,float) or not lo<=x<=hi or not math.isfinite(x):
        raise ValueError('Invalid real scalar')
    return float(x)

def validate_control_timestep(record, observation_size):
    _integer(observation_size,1,4096)
    if type(record) is not dict or len(record)>16 or any(type(k) is not str for k in record):
        raise ValueError('Invalid record envelope')
    required={'step_type','reward','discount','observation'}
    issues=['missing:'+k for k in required-record.keys()]+['unexpected:'+k for k in record.keys()-required]
    step=record.get('step_type');valid_step=type(step) is int and step in (0,1,2)
    if 'step_type' in record and not valid_step:issues.append('invalid:step_type')
    if 'observation' in record:
        try:
            obs=_float_array(record['observation'],1)
            if obs.shape!=(observation_size,):raise ValueError('Shape')
        except ValueError:issues.append('invalid:observation')
    if valid_step:
        for key,lo,hi in [('reward',-1e6,1e6),('discount',0,1)]:
            if key not in record:continue
            try:
                if step==0:
                    if record[key] is not None:raise ValueError('FIRST has no reward/discount')
                else:_real(record[key],lo,hi)
            except ValueError:issues.append('invalid:'+key)
    return sorted(issues)
