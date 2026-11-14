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

def interpolate_support(start,end,duration,fractions):
    a=_array(start,2);b=_array(end,2);u=_array(fractions,1);t=_scalar(duration,1e-3,100)
    if not 1<=len(a)<=16 or a.shape[1]!=2 or b.shape!=a.shape or len(u)>4096 or np.any((u<0)|(u>1)):raise ValueError("support interval")
    u=u[:,None];q0=a[:,0];v0=a[:,1];q1=b[:,0];v1=b[:,1]
    q=(2*u**3-3*u*u+1)*q0+(u**3-2*u*u+u)*t*v0+(-2*u**3+3*u*u)*q1+(u**3-u*u)*t*v1
    v=((6*u*u-6*u)*q0+(3*u*u-4*u+1)*t*v0+(-6*u*u+6*u)*q1+(3*u*u-2*u)*t*v1)/t
    return dict(position=q,velocity=v)
