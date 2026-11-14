import math

import re

import numpy as np

def _float_array(x,ndim):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:raise ValueError('Expected floating array')
    return x.astype(np.float64)

def _bool_array(x,shape):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('bool') or x.shape!=shape:raise ValueError('Expected Boolean array')
    return x

def _bounded(x,lo,hi):
    if not np.all(np.isfinite(x)) or np.any(x<lo) or np.any(x>hi):raise ValueError('Invalid numerical values')

def continual_transfer_report(rates, observed):
    r=_float_array(rates,2)
    if not 1<=r.shape[1]<=256 or r.shape[0]!=r.shape[1]+1:raise ValueError('Invalid history shape')
    mask=_bool_array(observed,r.shape);_bounded(r[mask],0,1);k=r.shape[1]
    forward=np.full(k,np.nan);backward=np.full(k,np.nan);forgetting=np.full(k,np.nan)
    for j in range(k):
        if j>=1 and mask[j,j] and mask[0,j]:forward[j]=r[j,j]-r[0,j]
        if j<k-1 and mask[k,j] and mask[j+1,j]:backward[j]=r[k,j]-r[j+1,j]
        if j<k-1 and np.all(mask[j+1:k+1,j]):forgetting[j]=np.max(r[j+1:k+1,j])-r[k,j]
    def mean(values):
        finite=values[np.isfinite(values)]
        return float(np.mean(finite)) if len(finite) else float('nan')
    return dict(forward=forward,backward=backward,forgetting=forgetting,forward_mean=mean(forward),backward_mean=mean(backward),forgetting_mean=mean(forgetting),final_mean=mean(r[k,mask[k]]))
