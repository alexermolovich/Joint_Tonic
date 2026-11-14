import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x,low,high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def gate_loop_closures(residuals, covariance, overlap, elapsed, threshold, min_overlap, min_elapsed):
    r=_array(residuals,2);c=_array(covariance,3);o=_array(overlap,1);t=_array(elapsed,1);gate=_scalar(threshold,0,1e6);omin=_scalar(min_overlap,0,1);tmin=_scalar(min_elapsed,0,1e6);k=len(r)
    if k>8192 or r.shape!=(k,6) or c.shape!=(k,6,6) or o.shape!=(k,) or t.shape!=(k,) or np.any((o<0)|(o>1)) or np.any((t<0)|(t>1e6)) or not np.allclose(c,c.swapaxes(1,2),atol=1e-9,rtol=0):raise ValueError("loop evidence contract")
    c=(c+c.swapaxes(1,2))/2;eig=np.linalg.eigvalsh(c)
    if np.any(eig[:,0]<np.maximum(1e-9,eig[:,-1]*1e-8)):raise ValueError("positive conditioned covariance required")
    solved=np.linalg.solve(c,r[...,None])[...,0];d=np.sum(r*solved,axis=1);reason=np.zeros(k,np.int64);reason[d>gate]=3;reason[o<omin]=2;reason[t<tmin]=1
    return dict(squared_distance=d,accepted=reason==0,reason=reason)
