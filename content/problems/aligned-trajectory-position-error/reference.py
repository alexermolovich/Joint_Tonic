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

def align_trajectory(estimated,reference,fit_scale):
    x=_array(estimated,2);y=_array(reference,2);n=len(x)
    if not 3<=n<=8192 or x.shape!=(n,3) or y.shape!=x.shape or type(fit_scale) is not bool:raise ValueError("trajectory alignment contract")
    mx=x.mean(axis=0);my=y.mean(axis=0);xc=x-mx;yc=y-my;variance=float(np.sum(xc*xc)/n)
    if variance<=1e-9:raise ValueError("insufficient estimated spread")
    u,s,vt=np.linalg.svd(yc.T@xc/n)
    if s[1]<=1e-9:raise ValueError("degenerate paired alignment")
    signs=np.array([1.,1.,-1. if np.linalg.det(u@vt)<0 else 1.]);rotation=(u*signs)@vt;scale=float(np.sum(s*signs)/variance) if fit_scale else 1.
    if scale<=1e-9:raise ValueError("unsupported alignment scale")
    translation=my-scale*(rotation@mx);aligned=scale*(x@rotation.T)+translation;error=np.linalg.norm(aligned-y,axis=1)
    return dict(rotation=rotation,translation=translation,scale=scale,aligned=aligned,errors=error,rmse=float(np.sqrt(np.mean(error*error))))
