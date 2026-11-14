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

def initialization_rank(jacobian,parameter_scales,measurement_std,relative_cutoff):
    j=_array(jacobian,2);scales=_array(parameter_scales,1);std=_array(measurement_std,1);cut=_scalar(relative_cutoff,1e-12,.01);r,d=j.shape
    if r>4096 or not 1<=d<=32 or scales.shape!=(d,) or std.shape!=(r,) or np.any(np.abs(j)>1000) or np.any((scales<1e-6)|(scales>1000)) or np.any((std<1e-6)|(std>1000)):raise ValueError("initialization linearization contract")
    a=j*scales[None,:]/std[:,None];_,s,vt=np.linalg.svd(a,full_matrices=False);rank=int(np.sum(s>cut*s[0])) if len(s) and s[0]>0 else 0;values=np.zeros(d);values[:len(s)]=s;retained=vt[:rank];projector=np.eye(d)-retained.T@retained
    return dict(singular_values=values,rank=rank,observable=rank==d,condition=float(s[0]/s[-1]) if rank==d else float('inf'),unobservable_projector=projector)
