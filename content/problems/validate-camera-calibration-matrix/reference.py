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

def validate_camera_matrix(K, width, height):
    K=_real(K)
    if K.shape!=(3,3): raise ValueError("Expected 3x3 matrix")
    for n in (width,height):
        if isinstance(n,(bool,np.bool_)) or not isinstance(n,(int,np.integer)) or not 1<=n<=100000: raise ValueError("Invalid image size")
    return bool(K[0,0]>0 and K[1,1]>0 and 0<=K[0,2]<width and 0<=K[1,2]<height and np.all(np.abs(K[[1,2,2],[0,0,1]])<=1e-9) and abs(K[2,2]-1)<=1e-9)
