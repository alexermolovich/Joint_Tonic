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

def marginalize_window(normal_matrix,rhs,retained):
    h=_array(normal_matrix,2);b=_array(rhs,1);d=len(h);a=retained
    if not 2<=d<=96 or h.shape!=(d,d) or b.shape!=(d,) or type(a) is not int or not 1<=a<d or not np.allclose(h,h.T,atol=1e-9,rtol=0):raise ValueError("normal equation contract")
    h=(h+h.T)/2;values=np.linalg.eigvalsh(h)
    if values[0]<max(1e-8,values[-1]*1e-8):raise ValueError("normal matrix conditioning")
    aa=h[:a,:a];ab=h[:a,a:];ba=h[a:,:a];bb=h[a:,a:];cross=np.linalg.solve(bb,ba);offset=np.linalg.solve(bb,b[a:]);normal=aa-ab@cross;reduced=b[:a]-ab@offset;xa=np.linalg.solve(normal,reduced);xb=np.linalg.solve(bb,b[a:]-ba@xa)
    return dict(normal=normal,reduced_rhs=reduced,retained_step=xa,removed_step=xb,constant_shift=float(-.5*(b[a:]@offset)))
