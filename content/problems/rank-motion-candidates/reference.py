import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int, float) or not low <= x <= high or not np.isfinite(x):
        raise ValueError("Scalar outside contract")
    return float(x)

def rank_trajectories(endpoint_error,collision_free,limits_ok,objective,endpoint_tolerance):
    error=_array(endpoint_error,1);collision=_array(collision_free,1,"b");limits=_array(limits_ok,1,"b");cost=_array(objective,1);tol=_scalar(endpoint_tolerance,0,1e6)
    if len(error)>100000 or collision.shape!=error.shape or limits.shape!=error.shape or cost.shape!=error.shape or np.any(error<0) or np.any(cost<0):raise ValueError("candidate contract")
    feasible=collision&limits&(error<=tol);ids=np.flatnonzero(feasible);order=ids[np.argsort(cost[ids],kind="stable")].astype(np.int64)
    return dict(feasible=feasible,order=order,best=int(order[0]) if len(order) else -1)
