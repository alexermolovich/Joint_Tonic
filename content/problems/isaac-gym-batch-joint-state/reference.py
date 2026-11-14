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

def batch_joint_states(flat_state, dof_indices):
    state=_float_array(flat_state,2);idx=_integer_array(dof_indices,2)
    if state.shape[1]!=2 or len(state)>100000 or idx.shape[0]>4096 or not 1<=idx.shape[1]<=256 or idx.size>min(len(state),100000):
        raise ValueError('Invalid state layout')
    if np.any(idx<0) or np.any(idx>=len(state)) or len(np.unique(idx))!=idx.size:
        raise ValueError('Indices must identify independent joints')
    return state[idx].copy()
