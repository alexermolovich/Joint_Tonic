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

def _homography(h):
    if h.shape[-2:]!=(3,3) or np.any(np.abs(h)>1000) or np.any(np.abs(np.linalg.det(h))<1e-9):raise ValueError("homography contract")
    return h

def _project(points,h):
    homogeneous=np.column_stack([points,np.ones(len(points))])@h.T;valid=np.abs(homogeneous[:,2])>1e-9
    uv=np.full((len(points),2),np.nan);uv[valid]=homogeneous[valid,:2]/homogeneous[valid,2,None]
    return uv,valid

def _size(size):
    size=_array(size,1,"i")
    if size.shape!=(2,) or np.any((size<1)|(size>4096)):raise ValueError("image size")
    return size

def _inside(p,size):
    return (p[:,0]>=0)&(p[:,0]<=size[1]-1)&(p[:,1]>=0)&(p[:,1]<=size[0]-1)

def keypoint_repeatability(source,target,target_from_source,source_size,target_size,threshold):
    a=_array(source,2);b=_array(target,2);h=_array(target_from_source,2);sa=_size(source_size);sb=_size(target_size);tau=_scalar(threshold,0,100)
    if a.shape[1]!=2 or b.shape[1]!=2 or len(a)>512 or len(b)>512 or h.shape!=(3,3) or not _inside(a,sa).all() or not _inside(b,sb).all():raise ValueError("repeatability contract")
    _homography(h);ab,va=_project(a,h);ba,vb=_project(b,np.linalg.inv(h));ea=va&_inside(ab,sb);eb=vb&_inside(ba,sa);ca=np.zeros(len(a),bool);cb=np.zeros(len(b),bool)
    if ea.any() and eb.any():
        ca[ea]=np.min(np.linalg.norm(ab[ea,None,:]-b[None,eb,:],axis=2),axis=1)<=tau
        cb[eb]=np.min(np.linalg.norm(ba[eb,None,:]-a[None,ea,:],axis=2),axis=1)<=tau
    denominator=int(ea.sum()+eb.sum());score=float((ca.sum()+cb.sum())/denominator) if denominator else float('nan')
    return dict(source_eligible=ea,target_eligible=eb,source_correct=ca,target_correct=cb,repeatability=score)
