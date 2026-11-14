import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def camera_health(received, residuals, valid, max_dropout, max_rmse):
    r=_array(received,2,"b");e=_array(residuals,3);v=_array(valid,2,"b")
    if not (1<=r.shape[0]<=16 and 1<=r.shape[1]<=4096) or e.shape!=(*r.shape,2) or v.shape!=r.shape or np.any(v&~r):raise ValueError("Observation contract")
    for x,hi in ((max_dropout,1),(max_rmse,1e6)):
        if type(x) not in (int,float) or not 0<=x<=hi:raise ValueError("Threshold")
    drop=(~r).mean(1);n=v.sum(1);err=np.sqrt(np.sum(np.sum(e*e,2)*v,1)/np.maximum(n,1))
    return dict(dropout_rate=drop,reprojection_rmse=err,observed=n>0,dropout_alert=drop>max_dropout,calibration_alert=(n>0)&(err>max_rmse))
