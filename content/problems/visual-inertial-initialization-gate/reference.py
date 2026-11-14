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

def validate_initialization(scale, gravity, gyro_bias, accel_bias, residuals, valid, jacobian, limits):
    s=_scalar(scale,1e-6,1000);g=_array(gravity,1);bg=_array(gyro_bias,1);ba=_array(accel_bias,1);r=_array(residuals,1);v=_array(valid,1,"b");j=_array(jacobian,2);lim=_array(limits,1);n=len(r)
    if g.shape!=(3,) or bg.shape!=(3,) or ba.shape!=(3,) or n>4096 or v.shape!=(n,) or j.shape[0]!=n or not 1<=j.shape[1]<=32 or np.any(np.abs(j)>1000) or lim.shape!=(7,):raise ValueError("initialization shape contract")
    if not 1e-6<=lim[0]<=lim[1]<=1000 or np.any((lim[2:6]<0)|(lim[2:6]>1000)) or not 1e-12<=lim[6]<=.01:raise ValueError("initialization limits")
    count=int(v.sum());singular=np.linalg.svd(j[v],compute_uv=False);rank=int(np.sum(singular>lim[6]*singular[0])) if len(singular) and singular[0]>0 else 0;rms=float(np.sqrt(np.mean(r[v]**2))) if count else float('nan');gravity_error=float(abs(np.linalg.norm(g)-9.81))
    checks=np.array([count>=j.shape[1] and rank==j.shape[1],lim[0]<=s<=lim[1],gravity_error<=lim[2],np.linalg.norm(bg)<=lim[3],np.linalg.norm(ba)<=lim[4],rms<=lim[5]],bool)
    return dict(count=count,rank=rank,rms=rms,gravity_error=gravity_error,checks=checks,accepted=bool(checks.all()))
