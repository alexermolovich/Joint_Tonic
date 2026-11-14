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

def masked_video_loss(predicted, target, valid):
    p=_float_array(predicted,5);y=_float_array(target,5)
    if p.shape!=y.shape:raise ValueError('Mismatched video')
    b,t,h,w,c=p.shape
    if b>256 or not 1<=t<=256 or not 1<=h<=64 or not 1<=w<=64 or c not in (1,3) or p.size>1000000:raise ValueError('Invalid video shape')
    mask=_bool_array(valid,(b,t));_bounded(p[mask],0,1);_bounded(y[mask],0,1)
    errors=np.zeros((b,t));errors[mask]=np.mean((p[mask]-y[mask])**2,axis=(1,2,3))
    counts=np.sum(mask,axis=0,dtype=np.int64);per=np.full(t,np.nan);np.divide(errors.sum(axis=0),counts,out=per,where=counts>0)
    total=int(counts.sum());loss=float(errors.sum()/total) if total else 0.
    return dict(loss=loss,per_horizon=per,frame_counts=counts,has_data=bool(total))
