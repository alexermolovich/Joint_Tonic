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

def feature_scores(source_descriptors,target_descriptors):
    a=_array(source_descriptors,2);b=_array(target_descriptors,2)
    if not 1<=a.shape[1]<=128 or b.shape[1]!=a.shape[1] or len(a)>1024 or len(b)>1024 or len(a)*len(b)>262144 or np.any(np.abs(a)>100) or np.any(np.abs(b)>100):raise ValueError("feature score contract")
    return (a@b.T)/np.sqrt(a.shape[1])
