import math

import numpy as np

def _float_array(x, ndim, bound=1e6):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:
        raise ValueError('Expected floating array with documented dimensions')
    y=x.astype(np.float64)
    if not np.all(np.isfinite(y)) or np.any(np.abs(y)>bound):
        raise ValueError('Invalid floating values')
    return y

def _integer_array(x, ndim):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('int64') or x.ndim!=ndim:
        raise ValueError('Expected int64 array')
    return x

def _boolean_array(x, shape):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('bool') or x.shape!=shape:
        raise ValueError('Expected matching Boolean array')
    return x

def reset_environment_batch(state, reset_state, done, episode_ids, steps):
    x=_float_array(state,2);z=_float_array(reset_state,2)
    if z.shape!=x.shape or x.shape[0]>4096 or not 1<=x.shape[1]<=256 or x.size>1000000:
        raise ValueError('Invalid reset state shapes')
    mask=_boolean_array(done,(len(x),));ids=_integer_array(episode_ids,1);ticks=_integer_array(steps,1)
    if ids.shape!=(len(x),) or ticks.shape!=ids.shape or np.any(ids<0) or np.any(ticks<0):
        raise ValueError('Invalid counters')
    if np.any(ids[mask]==np.iinfo(np.int64).max):raise ValueError('Episode counter overflow')
    out=x.copy();out[mask]=z[mask]
    next_ids=ids.copy();next_ids[mask]+=1
    next_ticks=ticks.copy();next_ticks[mask]=0
    return dict(state=out,episode_ids=next_ids,steps=next_ticks)
