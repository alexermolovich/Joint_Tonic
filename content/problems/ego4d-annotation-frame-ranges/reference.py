import math

import re

import numpy as np

def _int_array(x,ndim):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('int64') or x.ndim!=ndim:raise ValueError('Expected int64 array')
    return x

def annotation_frame_ranges(frame_times_ns, intervals_ns):
    times=_int_array(frame_times_ns,1);intervals=_int_array(intervals_ns,2)
    if len(times)>1000000 or intervals.shape[1]!=2 or len(intervals)>100000 or np.any(times<0) or np.any(times[1:]<=times[:-1]) or np.any(intervals<0) or np.any(intervals[:,0]>=intervals[:,1]):raise ValueError('Invalid video times or annotation intervals')
    return np.searchsorted(times,intervals,side='left').astype(np.int64)
