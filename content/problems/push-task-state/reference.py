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

def push_task_state(task_position,jacobian,joint_velocity):
    x=_array(task_position,1);j=_array(jacobian,2);v=_array(joint_velocity,1)
    if not 1<=len(x)<=16 or not 1<=len(v)<=16 or j.shape!=(len(x),len(v)):raise ValueError("task shape")
    return dict(position=x.copy(),velocity=j@v)
