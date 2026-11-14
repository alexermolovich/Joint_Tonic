import math

import re

import numpy as np

def _integer(x,lo,hi):
    if type(x) is not int or not lo<=x<=hi:raise ValueError('Invalid integer')
    return x

def _int_array(x,ndim):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('int64') or x.ndim!=ndim:raise ValueError('Expected int64 array')
    return x

def _float_array(x,ndim):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:raise ValueError('Expected floating array')
    return x.astype(np.float64)

def _bool_array(x,shape):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('bool') or x.shape!=shape:raise ValueError('Expected Boolean array')
    return x

def _bounded(x,lo,hi):
    if not np.all(np.isfinite(x)) or np.any(x<lo) or np.any(x>hi):raise ValueError('Invalid numerical values')

def video_transition_windows(images, actions, observed, episode_ids, starts, horizon):
    x=_float_array(images,4);a=_float_array(actions,2);ids=_int_array(episode_ids,1);begins=_int_array(starts,1);_integer(horizon,1,256)
    t,h,w,c=x.shape
    if not 1<=t<=4096 or not 1<=h<=64 or not 1<=w<=64 or c not in (1,3) or x.size>1000000:raise ValueError('Invalid image layout')
    if a.shape[0]!=t-1 or not 1<=a.shape[1]<=32 or ids.shape!=(t,) or len(begins)>4096:raise ValueError('Invalid sequence shape')
    obs=_bool_array(observed,(t,));_bounded(x,0,1);_bounded(a,-1e4,1e4)
    if np.any(ids<0) or np.any(ids[1:]<ids[:-1]) or np.any(begins<0) or np.any(begins>=t):raise ValueError('Invalid episode/start indices')
    s=len(begins);d=a.shape[1]
    if 2*s*horizon*h*w*c>1000000 or s*horizon*d>1000000:raise ValueError('Output budget')
    current=np.zeros((s,horizon,h,w,c));following=np.zeros_like(current);commands=np.zeros((s,horizon,d));valid=np.zeros((s,horizon),dtype=bool)
    for row,start in enumerate(begins):
        for k in range(horizon):
            frame=int(start)+k
            if frame+1<t and obs[frame] and obs[frame+1] and ids[frame]==ids[frame+1]==ids[start]:
                valid[row,k]=True;current[row,k]=x[frame];following[row,k]=x[frame+1];commands[row,k]=a[frame]
    return dict(current=current,next=following,actions=commands,valid=valid)
