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

def estimate_clock_offset(clock_a, clock_b):
    a,b=map(_real,(clock_a,clock_b))
    if a.ndim!=1 or b.shape!=a.shape or not len(a): raise ValueError("Need nonempty paired vectors")
    diff=b-a; offset=float(np.median(diff))
    return offset,diff-offset
