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

def distort_normalized_points(points, coefficients):
    points,c=map(_real,(points,coefficients))
    if points.ndim!=2 or points.shape[1]!=2 or c.shape!=(5,) or np.any(np.abs(points)>10) or np.any(np.abs(c)>1): raise ValueError("Invalid lens contract")
    x,y=points.T; k1,k2,p1,p2,k3=c; r2=x*x+y*y; radial=1+k1*r2+k2*r2**2+k3*r2**3
    return np.column_stack([x*radial+2*p1*x*y+p2*(r2+2*x*x),y*radial+p1*(r2+2*y*y)+2*p2*x*y])
