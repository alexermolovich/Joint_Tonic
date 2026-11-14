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

def seeded_return_summary(task_ids, seed_ids, returns):
    task=_integer_array(task_ids,1);seed=_integer_array(seed_ids,1);r=_float_array(returns,1)
    if len(r)>100000 or task.shape!=r.shape or seed.shape!=r.shape or np.any(task<0) or np.any(seed<0):
        raise ValueError('Invalid episode records')
    tasks,ti=np.unique(task,return_inverse=True);seeds,si=np.unique(seed,return_inverse=True)
    if len(tasks)*len(seeds)>1000000:raise ValueError('Grid too large')
    counts=np.zeros((len(tasks),len(seeds)),dtype=np.int64);sums=np.zeros(counts.shape,dtype=np.float64)
    np.add.at(counts,(ti,si),1);np.add.at(sums,(ti,si),r)
    means=np.full(counts.shape,np.nan,dtype=np.float64)
    np.divide(sums,counts,out=means,where=counts>0)
    task_means=np.array([np.mean(row[c>0]) for row,c in zip(means,counts)],dtype=np.float64)
    return dict(task_ids=tasks.copy(),seeds=seeds.copy(),counts=counts,means=means,task_means=task_means,overall=float(np.mean(task_means)) if len(tasks) else float('nan'))
