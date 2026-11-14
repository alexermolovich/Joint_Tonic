import numpy as np
import math

def compare_slice_regressions(slice_ids, baseline, candidate, slice_count, tolerance):
    if type(slice_count) is not int or not 1<=slice_count<=256 or type(tolerance) not in (int,float) or not 0<=tolerance<=1e6 or not math.isfinite(tolerance):raise ValueError('slice settings')
    if not isinstance(slice_ids,np.ndarray) or slice_ids.dtype!=np.int64 or slice_ids.ndim!=1 or len(slice_ids)>100000 or (slice_ids<0).any() or (slice_ids>=slice_count).any():raise ValueError('slice IDs')
    if any(not isinstance(a,np.ndarray) or a.dtype!=np.float64 or a.shape!=slice_ids.shape or not np.isfinite(a).all() or (a<0).any() or (a>1e6).any() for a in [baseline,candidate]):raise ValueError('paired loss arrays')
    delta=candidate-baseline;count=np.bincount(slice_ids,minlength=slice_count).astype(np.int64);sums=np.bincount(slice_ids,weights=delta,minlength=slice_count);means=np.full(slice_count,np.nan)
    np.divide(sums,count,out=means,where=count>0)
    return dict(counts=count,mean_delta=means,regressed=(count>0)&(means>tolerance),overall_delta=float(delta.mean()) if len(delta) else None,complete=bool(np.all(count>0)))
