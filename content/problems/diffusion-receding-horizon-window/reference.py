import numpy as np


def receding_horizon_window(trajectory, valid, offset, execute_steps):
    if not isinstance(trajectory,np.ndarray) or not isinstance(valid,np.ndarray):
        raise TypeError("trajectory and valid must be arrays")
    if type(offset) is not int or type(execute_steps) is not int:
        raise TypeError("offset and execute_steps must be built-in integers")
    if trajectory.ndim != 3 or trajectory.dtype not in (np.dtype("float32"),np.dtype("float64")):
        raise ValueError("trajectory must be float32/64 (B,H,D)")
    b,h,d=trajectory.shape
    if not (1<=b<=64 and 1<=h<=256 and 1<=d<=64) or trajectory.size>2_000_000:
        raise ValueError("dimensions outside bounds")
    if not np.isfinite(trajectory).all() or (np.abs(trajectory)>1e6).any():
        raise ValueError("invalid trajectory values")
    if valid.shape!=(b,h) or valid.dtype!=np.bool_:
        raise ValueError("valid must be bool (B,H)")
    if not (0<=offset<h and 1<=execute_steps<=h and offset+execute_steps<=h):
        raise ValueError("selected window outside horizon")
    if not valid[:,offset:offset+execute_steps].all():
        raise ValueError("selected window includes invalid commands")
    return trajectory[:,offset:offset+execute_steps,:].copy()
