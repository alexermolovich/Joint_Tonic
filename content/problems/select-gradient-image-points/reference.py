import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def select_gradient_points(image,tile_size,threshold):
    im=_array(image,2);h,w=im.shape;t=tile_size;tau=_scalar(threshold,0,1)
    if not 3<=h<=1024 or not 3<=w<=1024 or im.size>1000000 or type(t) is not int or not 1<=t<=128 or np.any((im<0)|(im>1)):raise ValueError("image selection contract")
    dx=(im[1:-1,2:]-im[1:-1,:-2])/2;dy=(im[2:,1:-1]-im[:-2,1:-1])/2;score=np.sqrt(dx*dx+dy*dy)
    y,x=np.nonzero(score>tau);scores=score[y,x];y=y+1;x=x+1;ids=y*w+x;tile=(y//t)*((w+t-1)//t)+x//t
    order=np.lexsort((ids,-scores,tile));groups=tile[order];first=np.r_[True,groups[1:]!=groups[:-1]] if len(order) else np.zeros(0,bool);chosen=order[first]
    return dict(coordinates=np.stack([x[chosen],y[chosen]],axis=1).astype(np.int64),scores=scores[chosen].copy())
