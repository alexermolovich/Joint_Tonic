import math

import re

import numpy as np

def _int_array(x,ndim):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('int64') or x.ndim!=ndim:raise ValueError('Expected int64 array')
    return x

def _float_array(x,ndim):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:raise ValueError('Expected floating array')
    return x.astype(np.float64)

def _bounded(x,lo,hi):
    if not np.all(np.isfinite(x)) or np.any(x<lo) or np.any(x>hi):raise ValueError('Invalid numerical values')

def cross_robot_prediction_error(robot_ids, episode_ids, squared_error, pixel_counts):
    robots=_int_array(robot_ids,1);episodes=_int_array(episode_ids,1);error=_float_array(squared_error,1);counts=_int_array(pixel_counts,1)
    if len(robots)>100000 or any(v.shape!=robots.shape for v in [episodes,error,counts]) or np.any(robots<0) or np.any(episodes<0) or np.any(counts<0) or np.any(counts>1000000000):raise ValueError('Invalid chunk evidence')
    _bounded(error,0,1e9)
    if np.any(error>counts):raise ValueError('Squared normalized-pixel residual exceeds support')
    ids=np.unique(robots);groups={int(key):{} for key in ids}
    for robot,episode,e,n in zip(robots,episodes,error,counts):
        entry=groups[int(robot)].setdefault(int(episode),[0.,0]);entry[0]+=float(e);entry[1]+=int(n)
    ep_count=[];pixels=[];pixel_mse=[];ep_mse=[]
    for key in ids:
        entries=[v for v in groups[int(key)].values() if v[1]>0];total=sum(v[1] for v in entries);ep_count.append(len(entries));pixels.append(total)
        pixel_mse.append(sum(v[0] for v in entries)/total if total else float('nan'))
        ep_mse.append(sum(v[0]/v[1] for v in entries)/len(entries) if entries else float('nan'))
    return dict(robot_ids=ids.copy(),episode_counts=np.array(ep_count,dtype=np.int64),pixel_counts=np.array(pixels,dtype=np.int64),pixel_mse=np.array(pixel_mse,dtype=np.float64),episode_mse=np.array(ep_mse,dtype=np.float64))
