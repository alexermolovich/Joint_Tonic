import numpy as np

def constrain_randomization_bounds(nominal, requested, allowed, margins):
    if any(not isinstance(x,np.ndarray) or x.dtype!=np.float64 or not np.isfinite(x).all() or (np.abs(x)>1e6).any() for x in [nominal,requested,allowed,margins]):raise ValueError('numeric arrays')
    if nominal.ndim!=1 or not 1<=len(nominal)<=64 or requested.shape!=(len(nominal),2) or allowed.shape!=requested.shape or margins.shape!=nominal.shape or (margins<0).any() or (requested[:,0]>requested[:,1]).any() or (allowed[:,0]>allowed[:,1]).any():raise ValueError('interval shape/order')
    lo=np.maximum(requested[:,0],allowed[:,0]+margins);hi=np.minimum(requested[:,1],allowed[:,1]-margins)
    feasible=(lo<=hi)&(lo<=nominal)&(nominal<=hi);bounds=np.column_stack((lo,hi));bounds[~feasible]=np.nan
    return dict(feasible=feasible,bounds=bounds,failed_dimensions=np.flatnonzero(~feasible).astype(np.int64))
