import numpy as np

def _real(value):
    try:
        a = np.asarray(value)
        if a.dtype.kind not in "iuf": raise ValueError("Expected real numeric data")
        a = a.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(a).all() or np.any(np.abs(a)>1e9):
        raise ValueError("Values must be finite with magnitude <=1e9")
    return a

def interpolate_pose(p0, q0, p1, q1, fraction):
    p0,a,p1,b,u=map(_real,(p0,q0,p1,q1,fraction))
    if p0.shape!=(3,) or p1.shape!=(3,) or a.shape!=(4,) or b.shape!=(4,) or u.ndim!=0 or not 0<=u<=1 or np.max(np.abs(a))==0 or np.max(np.abs(b))==0: raise ValueError("Invalid pose endpoints")
    a=a/np.max(np.abs(a)); a=a/np.linalg.norm(a); b=b/np.max(np.abs(b)); b=b/np.linalg.norm(b)
    dot=float(a@b)
    if dot<0: b=-b; dot=-dot
    dot=np.clip(dot,-1,1)
    if dot>.9995: q=(1-u)*a+u*b
    else:
        angle=np.arccos(dot); q=(np.sin((1-u)*angle)*a+np.sin(u*angle)*b)/np.sin(angle)
    return (1-u)*p0+u*p1,q/np.linalg.norm(q)
