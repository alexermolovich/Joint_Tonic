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

def _metric(m):
    if not np.allclose(m,m.swapaxes(-1,-2),atol=1e-10,rtol=0):raise ValueError("metric symmetry")
    eigen,vectors=np.linalg.eigh(.5*(m+m.swapaxes(-1,-2)))
    if np.any(eigen < -1e-10):raise ValueError("metric positivity")
    return (vectors*np.maximum(eigen,0)[...,None,:])@vectors.swapaxes(-1,-2)

def pullback_policy(jacobian,jacobian_rate,joint_velocity,task_metric,task_force):
    j=_array(jacobian,2);dj=_array(jacobian_rate,2);v=_array(joint_velocity,1);m=_array(task_metric,2);f=_array(task_force,1);t,d=j.shape
    if not 1<=t<=16 or not 1<=d<=16 or dj.shape!=j.shape or v.shape!=(d,) or m.shape!=(t,t) or f.shape!=(t,):raise ValueError("policy shape")
    m=_metric(m)
    return dict(metric=j.T@m@j,force=j.T@(f-m@(dj@v)))
